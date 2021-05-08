import logging
from csv import DictReader
from dataclasses import dataclass
from typing import List

from dataclass_csv import DataclassWriter

from socializer.data_augmentation import GenderClassifier
from socializer.google_contacts.manager import GoogleContactsManager
from socializer.models import Gender

logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s")

classifier = GenderClassifier()


@dataclass
class GenderUpdate:
    given_name: str
    gender: str
    etag: str
    resource_name: str


def generate_gender_updates() -> List[GenderUpdate]:
    gender_updates: List[GenderUpdate] = []
    with open("people.csv") as people_csv:
        reader = DictReader(people_csv)
        for person in reader:
            result = classifier.classify(name=person["given_name"])
            if result.probability < 90:
                logging.error(
                    "Name '%s' gender detected as '%s' with probability %s",
                    person["given_name"],
                    result.gender,
                    result.probability,
                )
            else:
                assert result.gender in Gender
                gender_updates.append(
                    GenderUpdate(
                        given_name=person["given_name"],
                        gender=result.gender,
                        etag=person["etag"],
                        resource_name=person["resource_name"],
                    )
                )
    return gender_updates


def save_gender_updates(updates: List[GenderUpdate]) -> None:
    with open("gender_updates.csv", "w") as gender_updates_csv:
        writer = DataclassWriter(gender_updates_csv, updates, GenderUpdate)
        writer.write()


def apply_gender_updates(updates: List[GenderUpdate]) -> None:
    gcontacts = GoogleContactsManager()
    for update in updates:
        gcontacts.update_gender(
            resource_name=update.resource_name,
            etag=update.etag,
            gender=Gender(update.gender),
        )


def main():
    updates = generate_gender_updates()
    save_gender_updates(updates=updates)
    apply_gender_updates(updates=updates)


main()
