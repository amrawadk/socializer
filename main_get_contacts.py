from dataclass_csv import DataclassWriter

from socializer.google_contacts import GoogleContactsAdapter
from socializer.models import Contact


def main():
    gcontacts_manager = GoogleContactsAdapter()
    contacts = gcontacts_manager.get_contacts_in_group(group_name="Family", limit=25)

    with open("contacts.csv", "w") as contacts_csv:
        writer = DataclassWriter(contacts_csv, contacts, Contact)
        writer.write()


main()
