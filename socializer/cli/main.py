"""Automation first approach to building and maintaing personal networks."""
from typing import List

import typer
from dataclass_csv import DataclassWriter
from PyInquirer import prompt

from socializer.cli.campaign import app as campaign_app
from socializer.cli.utils import _is_arabic
from socializer.data_augmentation import GenderClassifier
from socializer.google_contacts import GoogleContactsAdapter
from socializer.google_contacts.manager import GoogleContactsManager
from socializer.google_contacts.models import GooglePerson
from socializer.models import Contact, Gender

app = typer.Typer(name="socializer", help=__doc__)
app.add_typer(campaign_app)


def _fix_missing_genders(gmanager: GoogleContactsManager, people: List[GooglePerson]):
    classifier = GenderClassifier()
    for idx, person in enumerate(people):
        result = classifier.classify(name=person.given_name)
        message = "[{current}/{total}] Recommendation for '{name}' is '{gender}' ({probability}%)': ".format(
            current=idx + 1,
            total=len(people),
            name=person.given_name,
            gender=result.gender,
            probability=result.probability,
        )
        questions = [
            {
                "type": "expand",
                "message": message,
                "name": "gender",
                "default": "a",
                "choices": [
                    {"key": "a", "name": "Accept", "value": result.gender},
                    {"key": "m", "name": "Override to Male", "value": "male",},
                    {"key": "f", "name": "Override to Female", "value": "female"},
                ],
            }
        ]
        answers = prompt(questions)
        gmanager.update_gender(
            resource_name=person.resource_name,
            etag=person.etag,
            gender=Gender(answers["gender"]),
        )


def _check_missing_gender(gmanager: GoogleContactsManager, people: List[GooglePerson]):
    missing_gender = [c for c in people if c.gender is None]
    if missing_gender:
        questions = [
            {
                "type": "confirm",
                "message": f"Found {len(missing_gender)}/{len(people)} people with missing gender, Do you want to fix them?",
                "name": "fix_missing_gender",
                "default": True,
            },
        ]
        answers = prompt(questions)
        if answers["fix_missing_gender"]:
            _fix_missing_genders(gmanager=gmanager, people=missing_gender)
    else:
        typer.echo("All people have gender set!")


def _check_arabic_names(people: List[GooglePerson]):
    non_arabic = [c for c in people if not _is_arabic(name=c.given_name)]
    if non_arabic:
        typer.echo(
            f"Found {len(non_arabic)}/{len(people)} people with non arabic names!"
        )
    else:
        typer.echo("All people have arabic names!")


@app.command()
def analyze_group(name: str = typer.Option(...), limit: int = 20):
    """Analyze Google Contacts Group and optionally add any missing data."""
    gmanager = GoogleContactsManager()
    typer.echo(f"Analyzing contact group: {name} ...")

    people = gmanager.get_people_in_group(group_name=name, limit=limit)

    typer.echo(f"Found {len(people)} people in the group")

    _check_missing_gender(gmanager=gmanager, people=people)
    _check_arabic_names(people=people)


@app.command()
def export_contacts(
    group_name: str = typer.Option(...),
    output: typer.FileTextWrite = typer.Option("contacts.csv"),
    limit: int = 20,
):
    """Export Contacts in a google contact group to a csv file."""
    gcontacts_manager = GoogleContactsAdapter()
    contacts = gcontacts_manager.get_contacts_in_group(
        group_name=group_name, limit=limit
    )

    writer = DataclassWriter(output, contacts, Contact)
    writer.write()
    typer.echo(f"contacts written to {output.name}")


@app.command()
def export_people(
    group_name: str = typer.Option(...),
    output: typer.FileTextWrite = typer.Option("people.csv"),
    limit: int = 20,
):
    """Export People in a google contact group to a csv file.

    This includes more details than Contact"""
    gmanager = GoogleContactsManager()

    people = gmanager.get_people_in_group(group_name=group_name, limit=limit)

    writer = DataclassWriter(output, people, GooglePerson)
    writer.write()
    typer.echo(f"people written to {output.name}")


if __name__ == "__main__":
    app()
