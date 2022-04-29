import enum
from dataclasses import dataclass
from enum import Enum, EnumMeta
from typing import Optional


class MyEnumMeta(EnumMeta):
    def __contains__(cls, item):
        return item in [v.value for v in cls.__members__.values()]


class Gender(Enum, metaclass=MyEnumMeta):
    MALE = "male"
    FEMALE = "female"

    @classmethod
    def from_str(cls, string: str) -> Optional["Gender"]:
        gender = None
        if string in Gender:
            gender = Gender(string)
        return gender


@dataclass
class Contact:
    """Class for storing contact details.

    Attributes:
        full_name: the contact's full name, including both prefix and last names
        first_name: the contact's first name
        phone_num: This is used for whatsapp messaging
        prefix: An optional prefix or title, like `Dr.` or `Aunt`
        nickname: An optional nickname
        gender: the contact's gender
    """

    full_name: str
    first_name: str
    phone_num: str
    prefix: Optional[str] = None
    nickname: Optional[str] = None
    gender: Optional[Gender] = None


class ContactFilters(enum.Enum):
    """Supported ways to filter contacts"""

    GENDER_EXISTS = "gender"
    ARABIC_NAME = "arabic"


@dataclass
class Message:
    full_name: str
    phone_num: str
    body: str
