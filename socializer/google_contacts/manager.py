import os.path
from typing import Any, Iterable, List, Optional

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

    def get_people(self, limit: int = 1000) -> List[GooglePerson]:
        """Get a list of people in Google Contacts.

        Args:
            limit: limit for results, defaults to 1000 if not set.
        """

        # https://developers.google.com/people/api/rest/v1/people.connections/list#query-parameters
        max_page_size_for_google_api = 1000

        page_size = min(limit, max_page_size_for_google_api)

        people: List[GooglePerson] = []
        page_token = None
        while len(people) < limit:
            results = (
                self.service.people()
                .connections()
                .list(
                    resourceName="people/me",
                    personFields="names,phoneNumbers,genders",
                    pageSize=page_size,
                    pageToken=page_token,
                )
                .execute()
            )
            connections = results.get("connections", [])
            people.extend([GooglePerson(body=person) for person in connections])
            page_token = results.get("nextPageToken")

        return people[:limit]

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

        people: List[GooglePerson] = []

        # TODO figure out a better place for this variable
        resource_name_limit = 50
        for chunk in self._chunk(member_resource_names, resource_name_limit):
            response = (
                self.service.people()
                .getBatchGet(
                    resourceNames=chunk,
                    personFields="names,nicknames,phoneNumbers,genders",
                )
                .execute()
            )

            responses = response.get("responses")
            people.extend(
                [GooglePerson(body=response["person"]) for response in responses]
            )

        return people

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

    @staticmethod
    def _chunk(list_name: List[Any], size: int) -> Iterable[List[Any]]:
        for i in range(0, len(list_name), size):
            yield list_name[i : i + size]
