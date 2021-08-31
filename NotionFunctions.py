
import re
import requests
import json
from datetime import datetime
from getKeys import get_Keys

user_keys = get_Keys()
NOTION_DATABASE_ID = user_keys["NOTION_DATABASE_ID"]
NOTION_INTEGRATION_TOKEN = user_keys["NOTION_DATABASE_ID"]
headers = {
    'Authorization' : 'Bearer '+NOTION_INTEGRATION_TOKEN,
    'Content-Type' : "application/json",
    'Notion-Version': '2021-08-16'
}

def readDatabaase():
    readUrl = f'https://api.notion.com/v1/databases/{NOTION_DATABASE_ID}'
    results = request("GET", readUrl, headers=headers)
    print(results.status_code)

def createNotionPage(google_id, notes, task_title, due_date, status, archived):
    print(google_id)
    print(notes)
    print(task_title)
    print(due_date)
    print(status)
    print(archived)
    if notes == []:
        notes =""
    createUrl = f'https://api.notion.com/v1/pages'
    #api info: https://developers.notion.com/reference/page#property-value-object
    if validate_iso8601(due_date) is False:
        print("validate_iso8601")
        newPageData = {
            "parent": {"database_id": NOTION_DATABASE_ID},
            "properties" : {
                "Task Name": {
                    "title": [{
                        "type": "text",
                        "text": {
                            "content": task_title
                        }
                    }]
                },
                "Google Task ID": {
                    "rich_text": [{
                        "text": {
                            "content": google_id
                        }
                    }]
                },
                "Notes": {
                    "rich_text": [{
                        "text": {
                            "content": notes
                        }
                    }]
                },
                "Status": {
                    "checkbox": status
                }
            }
        }
    else:
        newPageData = {
            "parent": {"database_id": NOTION_DATABASE_ID},
            "properties" : {
                "Task Name": {
                    "title": [{
                        "type": "text",
                        "text": {
                            "content": task_title
                        }
                    }]
                },
                "Google Task ID": {
                    "rich_text": [{
                        "text": {
                            "content": google_id
                        }
                    }]
                },
                "Notes": {
                    "rich_text": [{
                        "text": {
                            "content": notes
                        }
                    }]
                },
                "Due Date" : {
                    "date": {
                        "start": due_date
                    }
                },
                "Status": {
                    "checkbox": status
                }
            }
        }
    data = json.dumps(newPageData)
    #print(str(uploadData))

    results = requests.request("POST", createUrl, headers = headers, data=data)
    print(results.status_code)
    print(results.json())

def updateNotionPage(page_id, google_id, notes, task_title, due_date, status, archived):
    print(page_id)
    print(google_id)
    print(notes)
    print(task_title)
    print(due_date)
    print(status)
    print(archived)
    if notes == []:
        notes =""

    createUrl = f'https://api.notion.com/v1/pages/{page_id}'
    # have keywards to control which properties to add
    #api info: https://developers.notion.com/reference/page#property-value-object
    if validate_iso8601(due_date) is False:
        print("validate_iso8601")
        newPageData = {
            "parent": {"database_id": NOTION_DATABASE_ID},
            "properties" : {
                "Task Name": {
                    "title": [{
                        "type": "text",
                        "text": {
                            "content": task_title
                        }
                    }]
                },
                "Google Task ID": {
                    "rich_text": [{
                        "text": {
                            "content": google_id
                        }
                    }]
                },
                "Notes": {
                    "rich_text": [{
                        "text": {
                            "content": notes
                        }
                    }]
                },
                "Status": {
                    "checkbox": status
                }
            }
        }
    else:
        newPageData = {
            "parent": {"database_id": NOTION_DATABASE_ID},
            "properties" : {
                "Task Name": {
                    "title": [{
                        "type": "text",
                        "text": {
                            "content": task_title
                        }
                    }]
                },
                "Google Task ID": {
                    "rich_text": [{
                        "text": {
                            "content": google_id
                        }
                    }]
                },
                "Notes": {
                    "rich_text": [{
                        "text": {
                            "content": notes
                        }
                    }]
                },
                "Due Date" : {
                    "date": {
                        "start": due_date
                    }
                },
                "Status": {
                    "checkbox": status
                }
            }
        }


    data = json.dumps(newPageData)
    #print(str(uploadData))

    results = requests.request("PATCH", createUrl, headers = headers, data=data)
    print(results.status_code)

def validate_iso8601(date):
    regex = r'^(-?(?:[1-9][0-9]*)?[0-9]{4})-(1[0-2]|0[1-9])-(3[01]|0[1-9]|[12][0-9])T(2[0-3]|[01][0-9]):([0-5][0-9]):([0-5][0-9])(\.[0-9]+)?(Z|[+-](?:2[0-3]|[01][0-9]):[0-5][0-9])?$'
    match_iso8601 = re.compile(regex).match
    try:
        if match_iso8601(date) is not None:
            return True
    except:
        pass
    return False
