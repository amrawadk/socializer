from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials


# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/contacts"]


def get_creds():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("secrets/token.json"):
        creds = Credentials.from_authorized_user_file("secrets/token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("secrets/credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("secrets/token.json", "w") as token:
            token.write(creds.to_json())

    return creds


def main():
    """Shows basic usage of the People API.
    Prints the name of the first 10 connections.
    """
    creds = get_creds()
    service = build("people", "v1", credentials=creds)

    results = (
        service.people()
        .connections()
        .list(resourceName="people/me", personFields="names,emailAddresses")
        .execute()
    )
    connections = results.get("connections", [])

    names = [person["names"][0].get("displayName") for person in connections]

    with open("contacts.txt", "w") as fh:
        fh.write("\n".join(names))


if __name__ == "__main__":
    main()