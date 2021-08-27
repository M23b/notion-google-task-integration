
import requests

#emulate the structure of the js apis

class SyncNotion():
    # Notion for Developers: https://developers.notion.com/reference/post-database-query
    def __init__(self, database_id, notion_url, integration_token):
        #self.name=name # instance attribute
        #self._name=name  # protected instance attribute need to use get and set methods if I do this
        self.database_id = database_id
        self.notion_url = notion_url
        self.integration_token = integration_token
        self.database_url = self.notion_url + self.database_id


        # vars build within the class
        #function to query databases
    def access_database(self):
        # prett much just tests the conenction to see if it works ... not sure how neccessary the function will be
        #database_url = self.notion_url + self.database_id
        print(self.database_url)
        response = requests.get(self.database_url, headers={"Authorization": f"{self.integration_token}", "Notion-Version": "2021-08-16" })
        #print(response.json())
        return(response.json())

    def query_database(self):
        # queries the entire database and returns it as a json file
        temp_url = self.database_url+"/query"
        # need to use post keyword when querying for some reason -> review request documentation
        response = requests.post(temp_url, headers={"Authorization": f"{self.integration_token}", "Notion-Version": "2021-08-16" })
        return(response.json())

class Database():
    """Parent Node of Tree"""
    def __init__(self, data_json):
        self.database = {}
        self.all_task_ids_dict = {}
        self.all_task_ids_list = []

        self.dObject = data_json['object'] # could have function calls here to sort each task
        self.results = []
        #self.initialize_results(data_json['results'])#: {Page(self.get_results())} # for page object in database object -> need new function
        for page in data_json['results']:
            self.results.append(page)
        #self.all_task_ids_list = [self.results] this is no use
        print(self.all_task_ids_list)
        #need a too string method

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
        #page[self.cover]: page_data_json[cover]
        #page[self.icon]: page_data_json[icon]
        self.parent = page_data_json['parent']
        self.archived = page_data_json['archived']
        self.properties = [Block(page_data_json['properties'])]

        Database.__init__(self)

        # need a too string method


class Block(Page):
    def __init__(self, block_data_json):
        self.block = {}
        #self.block[self.Overdue]: block_data_json['Overdue']
        #self.Overdue = block_data_json['Overdue']
        self.Related_to_Events_Associated_Tasks = block_data_json['Related_to_Events_Associated_Tasks']
        self.Course_Linked = block_data_json['Course_Linked']
        self.Task_Id = block_data_json['Task_Id']
        #self.Project_Tags = block_data_json['Project_Tags']
        self.Links = block_data_json['Links']
        self.Due_Date = block_data_json['Due_Date']
        #self.Related_to_Project_Table = block_data_json['Related_to_Project_Table']
        self.Google_Task_ID = block_data_json['Google_Task_ID']
        self.Status  = block_data_json['Status']
        #self.Hi_Priority = block_data_json['Hi_Priority']
        #self.Related_to_Job_Applications = block_data_json['Related_to_Job_Applications']
        #self.Duration_in_Minutes = block_data_json['Duration_in_Minutes']
        #self.People_Linked = block_data_json['Duration_in_Minutes']
        self.Task_Name = block_data_json['Task_Name']

        Page.__init__(self)

        self.task_dict[self.Task_Id] : { 'Google_Task_ID' : block_data_json['Google_Task_ID'],
                                                'Task_Name' : block_data_json['Task_Name'],
                                                'Due_Date' : block_data_json['Due_Date'],
                                                'Status' : block_data_json['Status'],
                                                'Course_Linked' : block_data_json['Course_Linked'],
                                                'Related_to_Events_Associated_Tasks' : block_data_json['Related_to_Events_Associated_Tasks'],
                                                'Links' : block_data_json['Links'],
                                                }
        print(self.task_dict.keys())

        #need a too string method
