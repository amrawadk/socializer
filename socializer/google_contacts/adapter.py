from typing import List

from socializer.google_contacts.manager import GoogleContactsManager
from socializer.models import Contact


class GoogleContactsAdapter:
    """Handles mapping functionality between google contacts and general domain

    This should not include any API interactions (should be delegated to the manager).
    TODO This should ideally also map the errors into general domain errors.
    """

    _manager: GoogleContactsManager

    def __init__(self) -> None:
        self._manager = GoogleContactsManager()

    def get_contacts_in_group(self, group_name: str, limit: int = 20) -> List[Contact]:
        people = self._manager.get_people_in_group(group_name=group_name, limit=limit)
        return [person.to_contact() for person in people]
