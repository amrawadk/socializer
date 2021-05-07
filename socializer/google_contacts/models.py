from dataclasses import dataclass
from socializer.models import Contact

@dataclass
class GooglePerson:
    """Google's representation of a person"""

    body: dict

    def to_contact(self) -> Contact:
        return Contact(
            name=self.body["names"][0].get("displayName"),
            phone_num=self.body["phoneNumbers"][0].get("canonicalForm"),
        )