from dataclass_csv import DataclassWriter

import socializer as sz
from socializer.models import Contact


def main():
    gcontacts = sz.GoogleContactsAdapter()
    contacts = gcontacts.get_contacts_in_group(group_name="Family", limit=25)

    with open("contacts.csv", "w") as f:
        w = DataclassWriter(f, contacts, Contact)
        w.write()


main()
