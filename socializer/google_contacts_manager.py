from typing import List
from socializer.models import Contact
import os.path
from typing import List
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials


class GoogleContactsManager:
    SCOPES = ["https://www.googleapis.com/auth/contacts.readonly"]

    def __init__(self) -> None:
        self.service = build("people", "v1", credentials=self._get_credentials())

    def get_contacts(self, limit: int = 20) -> List[Contact]:
        results = (
            self.service.people()
            .connections()
            .list(
                resourceName="people/me",
                personFields="names,phoneNumbers",
                pageSize=limit,
            )
            .execute()
        )
        connections = results.get("connections", [])

        contacts: List[Contact] = []
        for person in connections:
            contacts.append(
                Contact(
                    name=person["names"][0].get("displayName"),
                    phone_num=person["phoneNumbers"][0].get("canonicalForm"),
                )
            )
        return contacts

    def get_contacts_in_group(group_name: str) -> List[Contact]:
        ...

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
