"""Build messaging campaigns"""
from typing import List

from socializer.cli.utils import _is_arabic
from socializer.google_contacts import GoogleContactsAdapter
from socializer.models import Contact, FieldFilters


def _filter_required_fields(
    contacts: List[Contact], fields: List[FieldFilters]
) -> List[Contact]:
    filtered_contacts = [
        c for c in contacts if all((getattr(c, f.value) for f in fields))
    ]
    fields_str = [f.value for f in fields]
    print(
        f"{len(filtered_contacts)}/{len(contacts)} contacts matched the filters: '{' & '.join(fields_str)}'"
    )
    return filtered_contacts


def _filter_arabic_only_contacts(contacts: List[Contact]) -> List[Contact]:
    filtered_contacts = [c for c in contacts if _is_arabic(name=c.first_name)]
    print(
        f"{len(filtered_contacts)}/{len(contacts)} contacts matched the filter: 'arabic-only'"
    )
    return filtered_contacts


def generate_audience(
    group_names: List[str],
    fields: List[FieldFilters],
    arabic_only: bool = False,
    limit: int = 20,
) -> List[Contact]:
    gcontacts_manager = GoogleContactsAdapter()

    all_contacts: List[Contact] = []
    for group_name in group_names:
        contacts = gcontacts_manager.get_contacts_in_group(
            group_name=group_name, limit=limit
        )

        print(f"Found {len(contacts)} people in the group")

        if fields:
            contacts = _filter_required_fields(contacts=contacts, fields=fields)

        if arabic_only:
            contacts = _filter_arabic_only_contacts(contacts=contacts)

        all_contacts.extend(contacts)

    return all_contacts
