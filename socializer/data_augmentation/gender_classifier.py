import logging
from dataclasses import dataclass
from urllib.parse import quote

import requests_cache


@dataclass
class GenderClassification:
    gender: str
    probability: int


class GenderClassifier:
    def __init__(self) -> None:
        # TODO figure out an appropriate directory for the requests cache here
        # https://requests-cache.readthedocs.io/en/latest/user_guide.html#cache-name
        self._session = requests_cache.CachedSession("genderapi_cache")

    def classify(self, name: str) -> GenderClassification:
        response = self._session.get("https://genderapi.io/api/?name=" + quote(name))
        assert response.status_code == 200
        response_json = response.json()

        if "gender" not in response_json:
            # Can happen if there's a query limit reached for example
            # {'errmsg': 'query limit reached', 'errno': 93, 'status': False}
            logging.warning(
                "couldn't fetch gender predection for '%s', defaulting to male with zero probability",
                name,
            )
            return GenderClassification(gender="male", probability=0)

        return GenderClassification(
            gender=response_json["gender"], probability=response_json["probability"]
        )
