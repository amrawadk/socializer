from typing import List

import typer
from PyInquirer import prompt

from socializer.data_augmentation import GenderClassifier
from socializer.google_contacts.manager import GoogleContactsManager
from socializer.google_contacts.models import GooglePerson
from socializer.models import Gender

app = typer.Typer()
gmanager = GoogleContactsManager()
classifier = GenderClassifier()


def _fix_missing_genders(people: List[GooglePerson]):
    for person in people:
        result = classifier.classify(name=person.given_name)
        questions = [
            {
                "type": "expand",
                "message": f"Recommendation for '{person.given_name}' is '{result.gender}' ({result.probability}%)': ",
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


@app.command()
def analyze_group(name: str, limit: int = 20):
    typer.echo(f"Analyzing contact group: {name} ...")

    people = gmanager.get_people_in_group(group_name=name, limit=limit)

    typer.echo(f"Found {len(people)} people in the group")

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
            _fix_missing_genders(people=missing_gender)
    else:
        typer.echo("All people have gender set!")


if __name__ == "__main__":
    app()
