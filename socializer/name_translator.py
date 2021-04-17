from typing import List
from urllib.parse import quote
import requests

def tramslate_text_with_freetranslations_org(text: str) -> str:
    response = requests.get("https://www.freetranslations.org/translate/inc-ajax-translate.php?p1=en&p2=ar&p3=" + quote(text))
    assert response.status_code == 200
    return response.text


class NameTranslator:
    """Helps translate english names to arabic names, to be used in the messages"""
    @classmethod
    def translate_name(cls, name: str) -> str:
        return tramslate_text_with_freetranslations_org(text=name)

    @classmethod
    def translate_names(cls, names: List[str]) -> List[str]:
        return tramslate_text_with_freetranslations_org(text="\n".join(names)).split("\n")
