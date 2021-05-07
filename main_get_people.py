from dataclass_csv import DataclassWriter

from socializer.google_contacts.manager import GoogleContactsManager
from socializer.google_contacts.models import GooglePerson


def main():
    gcontacts_manager = GoogleContactsManager()
    people = gcontacts_manager.get_people_in_group(group_name="Family", limit=25)

    with open("people.csv", "w") as people_csv:
        writer = DataclassWriter(people_csv, people, GooglePerson)
        writer.write()


main()
