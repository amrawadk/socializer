from dataclasses import dataclass
from socializer.models import Contact


@dataclass
class GooglePerson:
    """Google's representation of a person"""

    body: dict

    @property
    def name(self) -> str:
        return self.body["names"][0].get("displayName")

    @property
    def phone_num(self) -> str:
        return self.body["phoneNumbers"][0].get("canonicalForm")

    def to_contact(self) -> Contact:
        return Contact(name=self.name, phone_num=self.phone_num,)
