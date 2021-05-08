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
    first_name: str
    phone_num: str
    prefix: Optional[str] = None
    gender: Optional[Gender] = None
