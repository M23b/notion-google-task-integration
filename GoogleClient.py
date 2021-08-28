from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

class GoogleClient():
    def __init__(self):
        self.service = None

    def set_up_service():
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

        self.service = build('tasks', 'v1', credentials=creds)

class TaskLists():
    def __init__(self, results_json):
        self.kind = results_json['kind']
        self.etag = results_json['etag']
        self.nextPageToken = results_json['nextPageToken']
        self.items = results_json['items'] # this is a list of all of the tasks

class Tasks():
    def __init__(self, items):
        self.kind = results_json['kind']
        self.id = results_json['id']
        self.etag = results_json['etag']
        self.title = results_json['title']
        self.updated = results_json['updated']
        self.selfLink = results_json['selfLink']
        self.position = results_json['position']
        self.notes = results_json['notes']
        self.status = results_json['status']
        self.due = results_json['due']

"""Add function to update (patch) a Task"""
"""Add function to delete (archieve) a Task"""

    # Call the Tasks API
    results = service.tasklists().list(maxResults=10).execute()
    items = results.get('items', [])
    print(items)
    task_list = service.tasks().list(tasklist='MDgyMDQzMTQxMzIyMTgyMDcxMzI6MDow', maxResults=10).execute()
    print("task list")
    print(task_list)
