"""Build messaging campaigns"""
from typing import Callable, Dict, List

import pyarabic.araby as araby
from mako.template import Template

from socializer.google_contacts import GoogleContactsAdapter
from socializer.models import Contact, ContactFilters, Message


def _is_arabic(name: str) -> bool:
    return all((c in araby.LETTERS for c in name.replace(" ", "")))


ContactFilterFun = Callable[[Contact], bool]
CONTACT_FILTERS: Dict[ContactFilters, ContactFilterFun] = {
    ContactFilters.GENDER_EXISTS: lambda contact: contact.gender is not None,
    ContactFilters.ARABIC_NAME: lambda contact: _is_arabic(name=contact.first_name),
}


def filter_contacts(
    contacts: List[Contact], filters: List[ContactFilters]
) -> List[Contact]:
    """Filter a list of contacts based on multiple filters"""
    for contact_filter in filters:
        old_len = len(contacts)
        contacts = [
            contact for contact in contacts if CONTACT_FILTERS[contact_filter](contact)
        ]
        print(
            f"{len(contacts)}/{old_len} contacts matched the filter: '{contact_filter}'"
        )

    return contacts


def get_contacts(
    group_names: List[str], filters: List[ContactFilters], limit: int = 20,
) -> List[Contact]:
    gcontacts_manager = GoogleContactsAdapter()

    all_contacts: List[Contact] = []
    for group_name in group_names:
        contacts = gcontacts_manager.get_contacts_in_group(
            group_name=group_name, limit=limit
        )

        print(f"Found {len(contacts)} people in the group")

        contacts = filter_contacts(contacts=contacts, filters=filters)

        all_contacts.extend(contacts)

    return all_contacts


def create_message(contact: Contact, template: Template) -> Message:
    return Message(
        full_name=contact.full_name,
        phone_num=contact.phone_num,
        body=template.render(**contact.__dict__),
    )
