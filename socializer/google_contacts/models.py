import logging
from dataclasses import dataclass
from typing import Dict, List, Optional

from socializer.google_contacts.errors import (
    GooglePersonHasMoreThanOneName,
    GooglePersonHasNoNames,
)
from socializer.models import Contact, Gender


@dataclass
class GoogleContactGroup:
    name: str
    resource_name: str


@dataclass
class GooglePerson:
    """Google's representation of a person"""

    # pylint: disable=too-many-instance-attributes
    # TODO see if this number can be reduced, perhaps we should more closely follow
    # the body, i.e have a 'Name' class, and a 'PhoneNumber' class.

    resource_name: str  # id in google contacts
    etag: str

    prefix: Optional[str]
    display_name: str
    given_name: str
    phone_num: str
    body: dict
    groups: List[GoogleContactGroup]
    gender: Optional[Gender] = None
    nickname: Optional[str] = None

    def __init__(
        self, body: dict, groups: Optional[List[GoogleContactGroup]] = None
    ) -> None:
        self.body = body
        self.display_name = self._get_display_name()
        self.prefix = self._get_prefix()
        self.given_name = self._get_given_name()
        self.phone_num = self._get_phone_num()
        self.nickname = self._get_nickname()
        self.resource_name = self.body["resourceName"]
        self.etag = self.body["etag"]
        self.gender = self._get_gender()
        self.groups = groups if groups else []

    def _get_display_name(self) -> str:
        return self._get_name_dict()["displayName"]

    def _get_prefix(self) -> Optional[str]:
        return self._get_name_dict().get("honorificPrefix")

    def _get_given_name(self) -> str:
        try:
            return self._get_name_dict()["givenName"]
        except KeyError:
            # TODO fix given name parsing
            logging.warning("failed to extract given name: %s", self.body)
            return ""

    def _get_phone_num(self) -> str:
        try:
            return self.body["phoneNumbers"][0]["canonicalForm"]
        except KeyError:
            # TODO fix phone number parsing
            logging.warning("failed to extract phone numbers: %s", self.body)
            return ""

    def _get_nickname(self) -> Optional[str]:
        nickname = None
        if self.body.get("nicknames"):
            nickname = self.body["nicknames"][0]["value"]
        return nickname

    def _get_name_dict(self) -> Dict[str, str]:
        # TODO figure out why name is missing
        if "names" not in self.body:
            logging.warning("name is missing from body: %s", self.body)
            return {"displayName": ""}

        if len(self.body["names"]) > 1:
            raise GooglePersonHasMoreThanOneName(person=self)
        if len(self.body["names"]) == 0:
            raise GooglePersonHasNoNames(person=self)
        return self.body["names"][0]

    def _get_gender(self) -> Optional[Gender]:
        gender = None
        if self.body.get("genders"):
            body_gender = self.body["genders"][0]["value"]
            gender = Gender.from_str(body_gender)
        return gender

    def to_contact(self) -> Contact:
        return Contact(
            full_name=self.display_name,
            prefix=self.prefix,
            first_name=self.given_name,
            phone_num=self.phone_num,
            gender=self.gender,
            nickname=self.nickname,
        )
