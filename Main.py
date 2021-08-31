
# imports for google client
from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from GoogleClient import TaskLists
from GoogleClient import Tasks
from GoogleClient import GoogleClient

import pandas as pd
import requests
import json
from datetime import datetime
import configparser
from getKeys import get_Keys

from NotionPyApi import Database, Page, Properties
from NotionFunctions import readDatabaase, createNotionPage, updateNotionPage

user_keys = get_Keys()
NOTION_DATABASE_ID = user_keys["NOTION_DATABASE_ID"]
NOTION_INTEGRATION_TOKEN = user_keys["NOTION_INTEGRATION_TOKEN"]
GOOGLE_TO_DO_DAILY_TASKLIST_ID = user_keys["GOOGLE_TO_DO_DAILY_TASKLIST_ID"]

print(NOTION_DATABASE_ID)
#print(NOTION_INTEGRATION_TOKEN)
print(GOOGLE_TO_DO_DAILY_TASKLIST_ID)
    #checks if a task in notion exists in google
    # -> also need to check if the task is archieved
def convert_notion_status(notion_status):
    if notion_status == False:
        return "needsAction"
    elif notion_status == True:
        return "completed"

def convert_google_status(google_status):
    if google_status == "needsAction":
        return False
    elif google_status == "completed":
        return True

# establish class instances of clients

# set up notion client

pDatabasejson = Database(NOTION_DATABASE_ID,
                            NOTION_INTEGRATION_TOKEN)
pDatabasejson.query_database() #print(pDatabasejson.results)
all_notion_task_json = pDatabasejson.results # all_task_json is a list of pages ( which are tasks - the properties portion of page hopes the data for each column)
all_notion_tasks_by_nKey = {}
all_notion_tasks_by_google_key = {}
created_goog_tasks = {}

for task in all_notion_task_json: # task is a dictionary that reprents the task row but also holds the properties which is another dictionary that holds the task stuff
    task_page = Page(task, NOTION_INTEGRATION_TOKEN) # retrieves the page object for the the task
    task_properties = Properties(task_page.properties, task['id'], task_page.last_edited_time, task_page.archived, task, NOTION_INTEGRATION_TOKEN) # retrieves the task page object's properties object
    print("line 55")
    print(task_properties.Google_Task_ID)
    try:
        all_notion_tasks_by_google_key[task_properties.Google_Task_ID] = task_properties

        print("line 57 main") # stores all notion task properties objects by google task id key
        print(task_properties.Google_Task_ID)
    except TypeError:
        print("google_task_id field is empty")
        print(task_properties)
# set up google client

gClient = GoogleClient()    # google client object
gClient.set_up_service()    # sets up oauth connection with google api
daily_to_do = TaskLists(gClient.service.tasks().list(tasklist=GOOGLE_TO_DO_DAILY_TASKLIST_ID, showDeleted = True, showHidden = True).execute()) # gets daily to do list from google tasks
print(daily_to_do.items)

all_google_tasks_by_google_key = {} # key google_task_id, val object -> holds all of the google task objects in a dictionary

for task in daily_to_do.items: # puts all of the google task objects into a dictionary with the id as the key and the object as the value
    print("task")
    print(task)
    daily_task = Tasks(task)
    all_google_tasks_by_google_key[daily_task.id] = daily_task

    if daily_task.id in all_notion_tasks_by_google_key:   # task already exists in notion -> if notion task google key matches the google task id then update the older task with the newer tasks info
        if all_notion_tasks_by_google_key[daily_task.id].last_edited_time > all_google_tasks_by_google_key[daily_task.id].updated: # notion task version was edited last
            print("notion task version was edited last")
            updated_task_body = {'status' : convert_notion_status(all_notion_tasks_by_google_key[daily_task.id].Status),
                            'kind' : "tasks#task",
                            'title' : all_notion_tasks_by_google_key[daily_task.id].Task_Name,
                            'due' : all_notion_tasks_by_google_key[daily_task.id].Due_Date,
                            'notes' : all_notion_tasks_by_google_key[daily_task.id].Notes,
                            'deleted' : all_notion_tasks_by_google_key[daily_task.id].archived,
                            'id': all_notion_tasks_by_google_key[daily_task.id].Google_Task_ID}
            print("updated_task_body")
            print(updated_task_body)
            temp_new_task_google = gClient.service.tasks().update(tasklist=GOOGLE_TO_DO_DAILY_TASKLIST_ID, task = daily_task.id, body = updated_task_body).execute() # update google task on google
        else: # google task is newer -> update notion task
            print("google task is newer -> update notion task")
            all_notion_tasks_by_google_key[daily_task.id].Status = convert_google_status(all_google_tasks_by_google_key[daily_task.id].status)
            all_notion_tasks_by_google_key[daily_task.id].Due_Date = all_google_tasks_by_google_key[daily_task.id].due
            all_notion_tasks_by_google_key[daily_task.id].Notes = all_google_tasks_by_google_key[daily_task.id].notes
            print("all_notion_tasks_by_google_key[daily_task.id].Notes")
            print(all_notion_tasks_by_google_key[daily_task.id].Notes)
            all_notion_tasks_by_google_key[daily_task.id].Task_Name = all_google_tasks_by_google_key[daily_task.id].title
            all_notion_tasks_by_google_key[daily_task.id].Google_Task_ID = all_google_tasks_by_google_key[daily_task.id].id
            all_notion_tasks_by_google_key[daily_task.id].archived = all_google_tasks_by_google_key[daily_task.id].deleted

            updateNotionPage(all_notion_tasks_by_google_key[daily_task.id].id, all_notion_tasks_by_google_key[daily_task.id].Google_Task_ID, all_notion_tasks_by_google_key[daily_task.id].Notes, all_notion_tasks_by_google_key[daily_task.id].Task_Name, all_notion_tasks_by_google_key[daily_task.id].Due_Date, all_notion_tasks_by_google_key[daily_task.id].Status, all_notion_tasks_by_google_key[daily_task.id].archived)

    else:# Google task does not exist in Notion
        print("Google task does not exist in Notion")
        print(all_google_tasks_by_google_key[daily_task.id])
        createNotionPage(all_google_tasks_by_google_key[daily_task.id].id, all_google_tasks_by_google_key[daily_task.id].notes, all_google_tasks_by_google_key[daily_task.id].title, all_google_tasks_by_google_key[daily_task.id].due, convert_google_status(all_google_tasks_by_google_key[daily_task.id].status), all_google_tasks_by_google_key[daily_task.id].deleted)
