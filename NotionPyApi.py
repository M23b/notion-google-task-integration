
import requests

#emulate the structure of the js apis

class Database():
    """Parent Node Database"""
    def __init__(self, database_id, notion_url, integration_token):
        # variables for syncing the database
        self.database_id = database_id
        self.notion_url = notion_url
        self.integration_token = integration_token
        self.database_url = self.notion_url + self.database_id
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
        temp_url = self.database_url+"/query"
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
        #function calls to create variables?
        #self.page[self.pObject]: page_data_json['object']
        self.pObject = page_data_json['object']
        self.id = page_data_json['id']
        self.created_time = page_data_json['created_time']
        self.last_edited_time = page_data_json['last_edited_time']
        self.parent = page_data_json['parent']
        self.archived = page_data_json['archived']
        self.properties = page_data_json['properties']
        self.Links = page_data_json['Links']
        self.Due_Date = page_data_json['Due_Date']
        self.Google_Task_ID = page_data_json['Google_Task_ID']
        self.Status  = page_data_json['Status']
        self.Task_Name = page_data_json['Task_Name']

        Database.__init__(self)



        # need a too string method


class Block(Page):
    def __init__(self, block_data_json, id):
        self.block = {}
        #self.block[self.Overdue]: block_data_json['Overdue']
        #self.Overdue = block_data_json['Overdue']
        self.Task_ID = id
        #self.Project_Tags = block_data_json['Project_Tags']
        #self.Links = block_data_json['Links']
        self.Due_Date = block_data_json['Due Date']
        #self.Related_to_Project_Table = block_data_json['Related_to_Project_Table']
        self.Google_Task_ID = block_data_json['Google Task ID']
        self.Status  = block_data_json['Status']
        #self.Hi_Priority = block_data_json['Hi_Priority']
        #self.Related_to_Job_Applications = block_data_json['Related_to_Job_Applications']
        #self.Duration_in_Minutes = block_data_json['Duration_in_Minutes']
        #self.People_Linked = block_data_json['Duration_in_Minutes']
        self.Task_Name = block_data_json['Task Name']

        #need a too string method
