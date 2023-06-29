"""Automation first approach to building and maintaing personal networks."""
from pathlib import Path
from typing import List

import typer
from dataclass_csv import DataclassWriter
from PyInquirer import prompt
from playwright.sync_api import sync_playwright

from socializer.cli.campaign import app as campaign_app
from socializer.data_augmentation import GenderClassifier
from socializer.google_contacts import GoogleContactsAdapter
from socializer.google_contacts.manager import GoogleContactsManager
from socializer.google_contacts.models import GooglePerson
from socializer.models import Contact, Gender
from socializer.services import _is_arabic

app = typer.Typer(name="socializer", help=__doc__)
main_app = typer.Typer(name="main")
app.add_typer(main_app)
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
        if result.probability > 90:
            typer.echo(message + "Accepting!")
            gender = Gender(result.gender)
        else:
            questions = [
                {
                    "type": "expand",
                    "message": message,
                    "name": "gender",
                    "default": "a",
                    "choices": [
                        {"key": "a", "name": "Accept", "value": result.gender},
                        {
                            "key": "m",
                            "name": "Override to Male",
                            "value": "male",
                        },
                        {"key": "f", "name": "Override to Female", "value": "female"},
                    ],
                }
            ]
            answers = prompt(questions)
            gender = Gender(answers["gender"])
        gmanager.update_gender(
            resource_name=person.resource_name,
            etag=person.etag,
            gender=gender,
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


@main_app.command()
def analyze_group(
    group_names: List[str] = typer.Option([], "--group-name", "-n"), limit: int = 20
):
    """Analyze Google Contacts Group and optionally add any missing data."""
    gmanager = GoogleContactsManager()

    for group_name in group_names:
        typer.echo(f"Analyzing contact group: {group_name} ...")

        people = gmanager.get_people_in_group(group_name=group_name, limit=limit)

        typer.echo(f"Found {len(people)} people in the group")

        _check_missing_gender(gmanager=gmanager, people=people)
        _check_arabic_names(people=people)


# TODO refactor this
@main_app.command()
def analyze_contacts():  # pylint: disable=too-many-locals
    """Analyze Google Contacts and optionally add any missing data."""
    gmanager = GoogleContactsManager()

    people = gmanager.get_people()
    groups = gmanager.get_groups()

    playwright = sync_playwright().start()

    # log into gcontacts if not logged in already
    gcontacts_storage_state_path = "playwright/.auth/gcontacts.json"

    contacts_browser = playwright.firefox.launch(headless=False)
    if not Path(gcontacts_storage_state_path).is_file():
        # I need to log in again
        contacts_page = contacts_browser.new_page()
        contacts_page.goto("https://contacts.google.com")
        input("hit 'Enter' once you're logged in")
        contacts_page.context.storage_state(path=gcontacts_storage_state_path)
    else:
        # I'm already logged in.
        contacts_page = contacts_browser.new_page(
            storage_state=gcontacts_storage_state_path
        )
        contacts_page.goto("https://contacts.google.com")

    # log into what's app if not logged in already
    # TODO figure out why this is not working
    whatsapp_storage_state_path = "playwright/.auth/whatsapp.json"

    whatsapp_browser = playwright.chromium.launch(headless=False)
    if not Path(whatsapp_storage_state_path).is_file():
        # I need to log in again
        whatsapp_page = whatsapp_browser.new_page()
        whatsapp_page.goto("https://web.whatsapp.com")
        input("hit 'Enter' when the browser is linked and the messages are open!")
        whatsapp_page.context.storage_state(path=whatsapp_storage_state_path)
    else:
        # I'm already logged in.
        whatsapp_page = whatsapp_browser.new_page(
            storage_state=whatsapp_storage_state_path
        )
        whatsapp_page.goto("https://web.whatsapp.com")

    group_choices = [dict(name=g.name, value=g.resource_name) for g in groups]

    # TODO ignore default group here.
    missing_group = [p for p in people if len(p.groups) < 1]
    typer.echo(f"Found {len(missing_group)} people in the group")

    for idx, person in enumerate(missing_group):
        person_id = person.resource_name.split("/")[1]

        contacts_page.goto(f"https://contacts.google.com/person/{person_id}")

        # Whatsapp requires a country code in the phone number, we're assuming it's all
        # Egypt for now.
        # TODO: this should be updates in the Google contacts to add a prefix based on the country.
        phone_no = person.phone_num
        if phone_no.startswith("00"):
            phone_no = f"+{phone_no[2:]}"

        if not phone_no.startswith("+"):
            phone_no = f"+2{phone_no}"

        whatsapp_page.goto(f"https://web.whatsapp.com/send?phone={phone_no}")

        message = """[{current}/{total}] Choose action for '{name}': """.format(
            current=str(idx + 1),
            total=len(missing_group),
            name=person.display_name,
        )

        questions = [
            {
                "type": "list",
                "message": message,
                "name": "action",
                "choices": [
                    {"name": "Delete", "value": "delete"},
                ]
                + group_choices,
            }
        ]
        answers = prompt(questions)
        action = answers["action"]

        if action == "delete":
            gmanager.delete_person(resource_name=person.resource_name)
        else:
            gmanager.add_person_to_group(person=person, group_resource_name=action)


@main_app.command()
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


@main_app.command()
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
