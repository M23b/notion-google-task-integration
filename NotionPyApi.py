
import requests

#emulate the structure of the js apis

class Database():
    """Parent Node Database"""
    def __init__(self, database_id, notion_db_url, integration_token):
        # variables for syncing the database
        self.database_id = database_id
        self.notion_db_url = notion_db_url
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
        self.dObject = self.data_json['object']
        self.results = self.data_json['results']
        #return(response.json())

    def initialize_results(self, data_json_results):
        results = []
        for page in data_json_results:
            results.append(page)
        return results


class Page(Database):
    """Child Node of Parent"""
    def __init__(self, page_data_json):
        self.page = {}
        self.notion_pg_url = "https://api.notion.com/v1/pages/"
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
        Database.__init__(self)

    def update_page(self, Due_Date, Google_Task_ID, Task_Name, Notes):
        #queries the entire database and returns it as a json file
        temp_url = self.notion_pg_url+self.id
        # need to use post keyword when querying for some reason -> review request documentation
        response = requests.post(temp_url, headers={"Authorization": f"{self.integration_token}",
        "Notion-Version": "2021-08-16"}, data = {'properties': {'Due Date': {'date' : {'start' : Due_Date}},
        'Google Task ID': {'rich_text' : Google_Task_ID}, 'Task Name': {'title' : ['text': {'content': Task_Name},
        'plain_text': Task_Name}]}, 'Notes': {'rich_text': Notes} })
        # need a too string method

"""Add function to delete (archieve) a page"""

class Properties(Page):
    def __init__(self, properties_data_json, id):
        self.properties_dict = {}
        #self.block[self.Overdue]: block_data_json['Overdue']
        #self.Overdue = block_data_json['Overdue']
        #self.Project_Tags = block_data_json['Project_Tags']
        #self.Links = block_data_json['Links']
        self.Notes = properties_data_json['Notes']['rich_text']
        self.Due_Date = properties_data_json['Due Date']['date']['start']
        #self.Related_to_Project_Table = block_data_json['Related_to_Project_Table']
        self.Google_Task_ID = properties_data_json['Google Task ID']['rich_text']
        self.Status  = properties_data_json['Status']['checkbox']
        #self.Hi_Priority = block_data_json['Hi_Priority']
        #self.Related_to_Job_Applications = block_data_json['Related_to_Job_Applications']
        #self.Duration_in_Minutes = block_data_json['Duration_in_Minutes']
        #self.People_Linked = block_data_json['Duration_in_Minutes']
        self.Task_Name = properties_data_json['Task Name']['title']['text']['plain_text']
        Page.__init__(self, id, last_edited_time, archived)
        #need a too string method
