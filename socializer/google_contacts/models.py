from dataclasses import dataclass
from typing import Optional

from socializer.google_contacts.errors import (
    GooglePersonHasMoreThanOneName,
    GooglePersonHasNoNames,
)
from socializer.models import Contact


@dataclass
class GooglePerson:
    """Google's representation of a person"""

    name: str
    prefix: Optional[str]
    given_name: str
    phone_num: str
    body: dict

    def __init__(self, body: dict) -> None:
        self.body = body
        self.name = self._get_name()
        self.prefix = self._get_prefix()
        self.given_name = self._get_given_name()
        self.phone_num = self._get_phone_num()

    def _get_name(self) -> str:
        return self._get_name_dict()["displayName"]

    def _get_prefix(self) -> Optional[str]:
        return self._get_name_dict().get("honorificPrefix")

    def _get_given_name(self) -> str:
        return self._get_name_dict()["givenName"]

    def _get_phone_num(self) -> str:
        return self.body["phoneNumbers"][0].get("canonicalForm")

    def _get_name_dict(self) -> dict[str, str]:
        if len(self.body["names"]) > 1:
            raise GooglePersonHasMoreThanOneName(person=self)
        if len(self.body["names"]) == 0:
            raise GooglePersonHasNoNames(person=self)
        return self.body["names"][0]

    def to_contact(self) -> Contact:
        return Contact(name=self.name, phone_num=self.phone_num)
