from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials


class GoogleClient():
    def __init__(self):
        self.service = self.set_up_service()

    def set_up_service(self):
        #quickstart from goog api - begin
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json')
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        return build('tasks', 'v1', credentials=creds)

class TaskLists():
    def __init__(self, results_json):
        self.kind = results_json['kind']
        self.etag = results_json['etag']
        self.nextPageToken = results_json['nextPageToken']
        self.items = results_json['items'] # this is a list of all of the tasks

class Tasks():
    def __init__(self, items):

        try:
            self.kind = items['kind']
        except KeyError:
            self.kind = ""

        try:
            self.id = items['id']
        except KeyError:
            self.id = ""

        try:
            self.etag = items['etag']
        except KeyError:
            self.etag = ""

        try:
            self.title = items['title']
        except KeyError:
            self.title = ""

        try:
            self.updated = items['updated']
        except KeyError:
            self.updated = ""

        try:
            self.selfLink = items['selfLink']
        except KeyError:
            self.selfLink = ""

        try:
            self.position = items['position']
        except KeyError:
            self.position = ""

        try:
            self.status = items['status']
        except KeyError:
            self.status = ""

        try:
            self.due = items['due']
        except KeyError:
            self.due = ""

        try:
            self.notes = items['notes']
        except KeyError:
            self.notes = ""

        try:
            self.deleted = items['deleted']
        except KeyError:
            self.deleted = False
"""
gClient = GoogleClient()    # google client object
gClient.set_up_service()
results = gClient.service.tasks().list(tasklist='MDgyMDQzMTQxMzIyMTgyMDcxMzI6MDow', maxResults=10).execute()
print(results)"""
