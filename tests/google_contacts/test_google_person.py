from typing import Optional

from faker import Faker

from socializer.google_contacts.models import GooglePerson
from socializer.models import Gender

faker = Faker()


class BaseTest:
    # pylint: disable=attribute-defined-outside-init
    # TODO is there a better way? I don't necessarily wanna lay those out fully
    # here, as it'd be too verbose with little to gain.
    def _generate_body(self, gender: Optional[str] = None) -> dict:
        self.display_name = faker.first_name()
        self.given_name = faker.first_name()
        self.phone_num = faker.phone_number()
        self.prefix = faker.prefix()
        self.etag = faker.pystr()
        self.resource_name = f"people/{faker.pystr()}"

        self.metadata = {
            "primary": True,
            "source": {"id": faker.pystr(), "type": "CONTACT"},
        }

        body = {
            "etag": self.etag,
            "names": [
                {
                    "displayName": self.display_name,
                    "displayNameLastFirst": faker.first_name(),
                    "givenName": self.given_name,
                    "metadata": self.metadata,
                    "unstructuredName": faker.first_name(),
                    "honorificPrefix": self.prefix,
                }
            ],
            "phoneNumbers": [
                {
                    "canonicalForm": self.phone_num,
                    "formattedType": "Mobile",
                    "metadata": self.metadata,
                    "type": "mobile",
                    "value": faker.phone_number(),  # This is different from canonical form
                }
            ],
            "resourceName": self.resource_name,
        }

        if gender:
            body["genders"] = [
                {
                    "formattedValue": gender.title(),
                    "metadata": self.metadata,
                    "value": gender,
                }
            ]

        return body


class TestBodyParsing(BaseTest):
    def test_non_existing_gender(self) -> None:
        body = self._generate_body()
        assert "genders" not in body

        person = GooglePerson(body=body)
        assert person.gender is None

    def test_male_gender(self) -> None:
        body = self._generate_body(gender="male")
        person = GooglePerson(body=body)
        assert person.gender == Gender.MALE

    def test_other_gender(self) -> None:
        body = self._generate_body(gender="other")
        person = GooglePerson(body=body)
        assert person.gender is None

    def test_etag_parsing(self) -> None:
        body = self._generate_body()
        person = GooglePerson(body=body)
        assert person.etag == self.etag

    def test_resource_name_parsing(self) -> None:
        body = self._generate_body()
        person = GooglePerson(body=body)
        assert person.resource_name == self.resource_name


class TestContactConversion(BaseTest):
    def test_conversion_to_contact(self) -> None:
        body = self._generate_body(gender="male")
        person = GooglePerson(body=body)

        contact = person.to_contact()

        assert contact.first_name == self.given_name
        assert contact.full_name == self.display_name
        assert contact.phone_num == self.phone_num
        assert contact.prefix == self.prefix
        assert contact.gender == Gender.MALE
