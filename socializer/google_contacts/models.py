from dataclasses import dataclass

from socializer.models import Contact


@dataclass
class GooglePerson:
    """Google's representation of a person"""

    name: str
    given_name: str
    phone_num: str
    body: dict

    def __init__(self, body: dict) -> None:
        self.body = body
        self.name = self._get_name()
        self.given_name = self._get_given_name()
        self.phone_num = self._get_phone_num()

    def _get_name(self) -> str:
        return self.body["names"][0].get("displayName")

    def _get_given_name(self) -> str:
        return self.body["names"][0].get("givenName")

    def _get_phone_num(self) -> str:
        return self.body["phoneNumbers"][0].get("canonicalForm")

    def to_contact(self) -> Contact:
        return Contact(name=self.name, phone_num=self.phone_num)
