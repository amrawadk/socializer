import logging
from typing import List

from dataclass_csv import DataclassReader, DataclassWriter

from socializer.data_augmentation import GenderClassifier
from socializer.models import Contact

logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s")

classifier = GenderClassifier()

contacts_with_gender: List[Contact] = []

with open("contacts.csv") as contacts_csv:
    reader = DataclassReader(contacts_csv, Contact)
    for contact in reader:
        gender_classification = classifier.classify(name=contact.first_name)
        if gender_classification.probability < 90:
            logging.error(
                "Name '%s' gender detected as '%s' with probability %s",
                contact.first_name,
                gender_classification.gender,
                gender_classification.probability,
            )
        else:
            contact.gender = gender_classification.gender
            contacts_with_gender.append(contact)

with open("contacts_with_gender.csv", "w") as contacts_with_gender_csv:
    writer = DataclassWriter(contacts_with_gender_csv, contacts_with_gender, Contact)
    writer.write()
