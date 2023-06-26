import os.path
from typing import Any, Iterable, List, Optional

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from socializer.google_contacts.errors import ContactGroupNotFound
from socializer.google_contacts.models import (
    GoogleContactGroup,
    GoogleContactGroupName,
    GoogleContactGroupResourceName,
    GooglePerson,
)
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
                    personFields="names,phoneNumbers,genders,memberships",
                    pageSize=page_size,
                    pageToken=page_token,
                )
                .execute()
            )
            connections = results.get("connections", [])

            groups_mapping = {g.resource_name: g.name for g in self._get_groups()}
            # TODO why is this special?
            groups_mapping["contactGroups/starred"] = "starred"

            for person in connections:
                # TODO: how can we improve the resolution of a value that's based on a call to a different API?
                groups = []
                for membership in person.get("memberships", []):
                    group_resource_name = membership["contactGroupMembership"][
                        "contactGroupResourceName"
                    ]
                    group_name = groups_mapping[group_resource_name]
                    groups.append(
                        GoogleContactGroup(
                            name=group_name, resource_name=group_resource_name
                        )
                    )

                people.append(GooglePerson(body=person, groups=groups))

            page_token = results.get("nextPageToken")

        return people[:limit]

    def _get_groups(self) -> List[GoogleContactGroup]:
        response = self.service.contactGroups().list().execute()
        contact_groups = response.get("contactGroups", [])
        return [
            GoogleContactGroup(name=g["name"], resource_name=g["resourceName"])
            for g in contact_groups
        ]

    def _get_group_resource_name_by_name(
        self, name: GoogleContactGroupName
    ) -> GoogleContactGroupResourceName:
        contact_groups = self._get_groups()

        group_resource_name = next(
            (group.resource_name for group in contact_groups if group.name == name),
            None,
        )
        if group_resource_name is None:
            raise ContactGroupNotFound(group_name=name)

        return group_resource_name

    def get_people_in_group(
        self, group_name: str, limit: int = 20
    ) -> List[GooglePerson]:
        group_resource_name = self._get_group_resource_name_by_name(name=group_name)

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
