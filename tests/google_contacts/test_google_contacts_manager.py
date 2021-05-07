import pytest
from socializer.google_contacts.manager import GoogleContactsManager
import socializer.google_contacts.errors as errors


class TestPeople:
    def test_getting_list_of_people(self) -> None:
        gcontacts = GoogleContactsManager()

        people = gcontacts.get_people(limit=5)
        assert len(people) == 5

class TestGroups:
    def test_non_existing_group_name_raises_exception(self) -> None:
        gcontacts = GoogleContactsManager()

        with pytest.raises(errors.ContactGroupNotFound):
            gcontacts.get_people_in_group(group_name="nonExistingGroup")
        

    def test_existing_group_returns_contacts(self) -> None:
        gcontacts = GoogleContactsManager()

        people = gcontacts.get_people_in_group(group_name="Family", limit=5)
        assert len(people) == 5

