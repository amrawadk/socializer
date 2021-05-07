from socializer.google_contacts.models import GooglePerson
from faker import Faker

faker = Faker()


def test_conversion_to_contact():
    display_name = faker.first_name()
    phone_num = faker.phone_number()

    metadata = {
        "primary": True,
        "source": {"id": faker.pystr(), "type": "CONTACT"},
    }
    person = GooglePerson(
        body={
            "etag": faker.pystr(),
            "names": [
                {
                    "displayName": display_name,
                    "displayNameLastFirst": faker.first_name(),
                    "givenName": faker.first_name(),
                    "metadata": metadata,
                    "unstructuredName": faker.first_name(),
                }
            ],
            "phoneNumbers": [
                {
                    "canonicalForm": phone_num,
                    "formattedType": "Mobile",
                    "metadata": metadata,
                    "type": "mobile",
                    "value": faker.phone_number(),  # This is different from canonical form
                }
            ],
            "resourceName": f"people/{faker.pystr()}",
        }
    )

    contact = person.to_contact()

    assert contact.name == display_name
    assert contact.phone_num == phone_num