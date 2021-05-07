from dataclasses import dataclass
from enum import Enum
from typing import Optional


class Gender(Enum):
    MALE = "male"
    FEMALE = "female"


@dataclass
class Contact:
    first_name: str
    phone_num: str
    prefix: Optional[str] = None
    gender: Optional[Gender] = None
