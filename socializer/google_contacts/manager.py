import os.path
from typing import List, Optional

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from socializer.google_contacts.errors import ContactGroupNotFound
from socializer.google_contacts.models import GooglePerson
from socializer.models import Gender


class GoogleContactsManager:
    """Handles all API interactions with Google Contacts.

    This should only be aware of google contacts errors and models, and not use any of the general models
    Appropriate mapping should be done in the adapter."""

    SCOPES = ["https://www.googleapis.com/auth/contacts"]

    def __init__(self) -> None:
        self.service = build("people", "v1", credentials=self._get_credentials())

    def get_people(self, limit: int = 20) -> List[GooglePerson]:
        results = (
            self.service.people()
            .connections()
            .list(
                resourceName="people/me",
                personFields="names,phoneNumbers,genders",
                pageSize=limit,
            )
            .execute()
        )
        connections = results.get("connections", [])
        return [GooglePerson(body=person) for person in connections]

    def get_people_in_group(
        self, group_name: str, limit: int = 20
    ) -> List[GooglePerson]:
        ## Get id of that group name
        response = self.service.contactGroups().list().execute()
        contact_groups = response.get("contactGroups", [])
        group_resource_name = next(
            (
                group["resourceName"]
                for group in contact_groups
                if group.get("name") == group_name
            ),
            None,
        )
        if group_resource_name is None:
            raise ContactGroupNotFound(group_name=group_name)

        ## Get members of that group
        response = (
            self.service.contactGroups()
            .get(resourceName=group_resource_name, maxMembers=limit)
            .execute()
        )

        # TODO: is this ever empty?
        member_resource_names = response["memberResourceNames"]

        response = (
            self.service.people()
            .getBatchGet(
                resourceNames=member_resource_names,
                personFields="names,phoneNumbers,genders",
            )
            .execute()
        )

        responses = response.get("responses")
        return [GooglePerson(body=response["person"]) for response in responses]

    def update_gender(
        self, resource_name: str, etag: str, gender: Optional[Gender]
    ) -> GooglePerson:
        gender_value = "other" if gender is None else gender.value

        response = (
            self.service.people()
            .updateContact(
                resourceName=resource_name,
                updatePersonFields="genders",
                body={"etag": etag, "genders": [{"value": gender_value}]},
            )
            .execute()
        )

        return GooglePerson(body=response)

    def _get_credentials(self):
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        # TODO: extract secrets directory into a class variable
        if os.path.exists("secrets/token.json"):
            creds = Credentials.from_authorized_user_file(
                "secrets/token.json", self.SCOPES
            )
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "secrets/credentials.json", self.SCOPES
                )
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open("secrets/token.json", "w") as token:
                token.write(creds.to_json())

        return creds
