import csv
import logging
from urllib.parse import quote

import requests
import requests_cache

requests_cache.install_cache("genderapi_cache")

logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s")


def detect_gender(name: str) -> dict:
    response = requests.get("https://genderapi.io/api/?name=" + quote(name))
    assert response.status_code == 200
    response_json = response.json()

    if response_json["probability"] < 90:
        logging.error(
            "Name '%s' gender detected as '%s' with probability %s",
            name,
            response_json["gender"],
            response_json["probability"],
        )

    return response.json()["gender"]


with open("people.csv") as people_csv:
    reader = csv.DictReader(people_csv)
    for row in reader:
        print(row["given_name"], detect_gender(name=row["given_name"]))
