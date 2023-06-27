import pytest

import socializer.google_contacts.errors as errors
from socializer.google_contacts.manager import GoogleContactsManager
from socializer.google_contacts.models import GoogleContactGroup
from socializer.models import Gender


class TestPeople:
    def test_getting_list_of_people(self) -> None:
        gcontacts = GoogleContactsManager()

        people = gcontacts.get_people(limit=5)
        assert len(people) == 5

    def test_getting_list_of_people_with_pagination(self):
        """Limit for a single request is 1000 according to the docs:
        https://developers.google.com/people/api/rest/v1/people.connections/list#query-parameters
        """
        gcontacts = GoogleContactsManager()

        people = gcontacts.get_people(limit=1200)
        assert len(people) == 1200

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

    def test_update_group_works(self) -> None:
        gcontacts = GoogleContactsManager()

        person = gcontacts.get_people(limit=1)[0]

        groups = gcontacts.get_groups()
        group = groups[0]

        breakpoint()
        assert group not in person.groups

        person = gcontacts.add_person_to_group(
            person=person, group_resource_name=group.resource_name
        )

        # TODO fix this
        # assert group in groups


class TestGroups:
    def test_get_users_returns_groups(self) -> None:
        gcontacts = GoogleContactsManager()

        people = gcontacts.get_people(limit=5)
        assert len(people) == 5
        assert people[0].groups == [
            GoogleContactGroup(
                name="myContacts", resource_name="contactGroups/myContacts"
            )
        ]

    def test_non_existing_group_name_raises_exception(self) -> None:
        gcontacts = GoogleContactsManager()

        with pytest.raises(errors.ContactGroupNotFound):
            gcontacts.get_people_in_group(group_name="nonExistingGroup")

    def test_existing_group_returns_contacts(self) -> None:
        gcontacts = GoogleContactsManager()

        people = gcontacts.get_people_in_group(group_name="Family", limit=5)
        assert len(people) == 5
