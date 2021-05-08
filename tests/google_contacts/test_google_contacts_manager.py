import pytest

import socializer.google_contacts.errors as errors
from socializer.google_contacts.manager import GoogleContactsManager
from socializer.models import Gender


class TestPeople:
    def test_getting_list_of_people(self) -> None:
        gcontacts = GoogleContactsManager()

        people = gcontacts.get_people(limit=5)
        assert len(people) == 5

    def test_update_gender_works(self) -> None:
        gcontacts = GoogleContactsManager()

        person = gcontacts.get_people(limit=1)[0]

        current_gender = person.gender
        desired_gender = Gender.FEMALE if current_gender == Gender.MALE else Gender.MALE

        assert person.gender != desired_gender

        person = gcontacts.update_gender(
            resource_name=person.resource_name, etag=person.etag, gender=desired_gender
        )
        assert person.gender == desired_gender

        # Clean up after test, to make sure it's not destructive
        person = gcontacts.update_gender(
            resource_name=person.resource_name, etag=person.etag, gender=current_gender
        )


class TestGroups:
    def test_non_existing_group_name_raises_exception(self) -> None:
        gcontacts = GoogleContactsManager()

        with pytest.raises(errors.ContactGroupNotFound):
            gcontacts.get_people_in_group(group_name="nonExistingGroup")

    def test_existing_group_returns_contacts(self) -> None:
        gcontacts = GoogleContactsManager()

        people = gcontacts.get_people_in_group(group_name="Family", limit=5)
        assert len(people) == 5
