import requests

#emulate the structure of the js apis

class Database():
    """Parent Node Database"""
    def __init__(self, database_id, integration_token):
        # variables for syncing the database
        self.database_id = database_id
        self.notion_db_url = "https://api.notion.com/v1/databases/"
        self.integration_token = integration_token
        self.cmplt_database_url = self.notion_db_url + self.database_id
        #self.data_json = self.query_database(database_url, integration_token)
        self.database = {}
        self.all_task_ids_dict = {}
        self.all_task_ids_list = []
        # variables that the NOTION JS API has that I need
        #
        self.data_json = None
        #  'object' is the type of object that json file contains on the outer layer (the parent class/node)
        self.dObject = None
        # 'results' contains a
        self.results = None

    def query_database(self):
        #queries the entire database and returns it as a json file
        temp_url = self.cmplt_database_url+"/query"
        # need to use post keyword when querying for some reason -> review request documentation
        response = requests.post(temp_url, headers={"Authorization": f"{self.integration_token}", "Notion-Version": "2021-08-16" })
        self.data_json = response.json()
        print(self.data_json)
        self.dObject = self.data_json['object']
        self.results = self.data_json['results']
        #return(response.json())

    def initialize_results(self, data_json_results):
        results = []
        for page in data_json_results:
            results.append(page)
        return results

class Page():
    """Child Node of Parent"""
    def __init__(self, page_data_json, integration_token):
        self.page = {}
        self.notion_pg_url = "https://api.notion.com/v1/pages/"
        self.integration_token = integration_token
        #function calls to create variables?
        #self.page[self.pObject]: page_data_json['object']
        self.pObject = page_data_json['object']
        self.id = page_data_json['id']
        self.created_time = page_data_json['created_time']
        self.last_edited_time = page_data_json['last_edited_time']
        self.cover = page_data_json['cover']
        self.parent = page_data_json['parent']['database_id']
        self.archived = page_data_json['archived']
        self.properties = page_data_json['properties']
        #Database.__init__(self, database_id, integration_token)

    def update_page(self):
        #queries the entire database and returns it as a json file
        temp_url = self.notion_pg_url+self.id
        # need to use post keyword when querying for some reason -> review request documentation
        response = requests.PATCH(temp_url, headers={"Authorization": f"{self.integration_token}",
        "Notion-Version": "2021-08-16"}, archived = self.archived, data = {'properties': {'Due Date': {'date' : {'start' : self.Due_Date}},
        'Google Task ID': {'rich_text' : Google_Task_ID}, 'Task Name' : {'title' : [{'text' : {'content': self.Task_Name},
        'plain_text': Task_Name}]}, 'Status': {'checkbox': status}, 'Notes': {'rich_text': self.Notes}}})
        # need a too string method

    def create_page(self, Due_Date, Google_Task_ID, Task_Name, Notes, archived_input, status):
        #queries the entire database and returns it as a json file
        temp_url = self.notion_pg_url+self.id
        # need to use post keyword when querying for some reason -> review request documentation
        response = requests.POST(temp_url, headers={"Authorization": f"{self.integration_token}",
        "Notion-Version": "2021-08-16"}, archived = archived_input, data = {'properties': {'Due Date': {'date' : {'start' : Due_Date}},
        'Google Task ID': {'rich_text' : self.Google_Task_ID}, 'Task Name' : {'title' : [{'text' : {'content': self.Task_Name},
        'plain_text': self.Task_Name}]}, 'Status': {'checkbox': self.status}, 'Notes': {'rich_text': self.Notes}}})

    # do I need an archieve/delete function?
"""Add function to delete (archieve) a page"""

class Properties(Page):
    def __init__(self, properties_data_json, page_id, last_edited_time, archived, page_data_json, integration_token):
        self.properties_dict = {}

        self.last_edited_time = last_edited_time
        self.archived = archived
        self.id = page_id
        self.Task_Name = properties_data_json['Task Name']['title'][0]['plain_text']
        self.Notes = self.set_Notes(properties_data_json['Notes']['rich_text'])
        self.Due_Date = self.set_due_date(properties_data_json['Due Date'])
        self.Google_Task_ID = self.set_Google_Task_ID(properties_data_json['Google Task ID']['rich_text'])
        self.Status  = properties_data_json['Status']['checkbox']
        self.page_data_json = page_data_json
        Page.__init__(self, page_data_json, integration_token)

        #need a too string method

    def set_due_date(self, properties_data_due_date):
        try:
            temp_due_date = properties_data_due_date['date']
            print("temp_due_date")
            print(self.Task_Name)
            print(properties_data_due_date['date'])
            ddate = temp_due_date['start']
            print("ddate")
            print(ddate)
        except TypeError:
            print("error in set due date")
            print(self.Task_Name)
            ddate = None
            print("ddate")
            print(ddate)
        return ddate

    def set_Google_Task_ID(self, properties_data_json_Google_Task_ID_rich_text):
        # properties_data_json_Google_Task_ID_rich_text -> [{'type': 'text', 'text': {'content': 'VWZoX0JuSzdjWTYzWnRseQ', 'link': None}, 'annotations': {'bold': False, 'italic': False, 'strikethrough': False, 'underline': False, 'code': False, 'color': 'default'}, 'plain_text': 'VWZoX0JuSzdjWTYzWnRseQ', 'href': None}]
        try:
            temp_id = properties_data_json_Google_Task_ID_rich_text[0]['plain_text']
            #print("temp_id")
            #print(temp_id)
            return temp_id
        except IndexError:
            return None

    def set_Notes(self, properties_data_json_Notes_rich_text):
        #'notes': [{'type': 'text', 'text': {'content': 'test test test', 'link': None}, 'annotations': {'bold': False, 'italic': False, 'strikethrough': False, 'underline': False, 'code': False, 'color': 'default'}, 'plain_text': 'test test test', 'href': None}]
        try:
            temp_notes = properties_data_json_Notes_rich_text[0]['plain_text']
            #print("temp_id")
            #print(temp_id)
            return temp_notes
        except TypeError:
            return ""
