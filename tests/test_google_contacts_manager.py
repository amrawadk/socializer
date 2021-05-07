import pytest
import socializer as sz
import socializer.errors as errors

def test_non_existing_group_name_raises_exception() -> None:
    gcontacts = sz.GoogleContactsManager()

    with pytest.raises(errors.ContactGroupNotFound):
        gcontacts.get_contacts_in_group(group_name="nonExistingGroup")
    

def test_existing_group_returns_contacts() -> None:
    gcontacts = sz.GoogleContactsManager()

    contacts = gcontacts.get_contacts_in_group(group_name="Family", limit=5)
    assert len(contacts) == 5

    
