from socializer.models import Gender, Contact
from typing import List

class MockContactsRepository:
    contacts = {
        "test-id": Contact(
                id="test-id",
                full_name="Test Full Name",
                first_name="Test",
                phone_num="+201117823728",
                gender=Gender.FEMALE,
            )
    }
    def list_contacts(self, limit: int) -> List[Contact]:
        return list(self.contacts.values())[:limit]

class MockNamePredectionRepository:
    def predict_gender



class TestPeopleManagement:
    def test_can_change_gender(self):
        contacts_repository = MockContactsRepository()
        contact_manager_service = ContactManagerService(
            contacts_repository=contacts_repository
        )

        contact = ContactManagerService.list_contacts(limit=1)
        old_gender = contact.gender

        new_gender = Gender.MALE if old_gender == Gender.FEMALE else Gender.FEMALE
        contact = ContactManagerService.set_gender(id=contact.id, gender=new_gender)
        assert contact.gender == new_gender

        contact = ContactManagerService.set_gender(id=contact.id, gender=old_gender)
        assert contact.gender == old_gender

    def test_gender_predection(self):
        contact = ContactManagerService.list_contacts(limit=1)

        predicted_gender = NamePredictorService.predict_gender(name=contact.name)


