
import requests
# How to Use the Python Requests Module With REST APIs: https://www.nylas.com/blog/use-python-requests-module-rest-apis/
#
#class ClassName(object):
#    """docstring for ."""
#
#    def __init__(self, arg):
#        super(, self).__init__()
#        self.arg = arg

"""
> Notion DB Structure: https://developers.notion.com/docs/working-with-databases
"""
class NotionAPI():
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

    def get_task_id(self,data_json,index):
        return data_json["results"][index]["id"]

    def retrieve_task_ids(self,data_json):
        all_task_ids = []
        more_tasks = True
        count = 0
        for task in data_json:
            print(data_json["results"][count]["id"])
            count = count + 1
            #except IndexError:

    def get_all_tasks(self, data_json):
        all_tasks = {}
        for task in data_json['results']:
            test = []
            #print(data_json['results']['id'])
            task = frozenset(task.items())
            notion_id = data_json[task]['id']
            Task_Name = data_json[task]['properties']['Task Name']
            Due_Date = data_json[task]['properties']['Due Date']
            Notes = data_json[task]['properties']['Notes']
            Google_Task_ID = data_json[task]['properties']['Google Task ID']
            test = [notion_id, Task_Name, Due_Date, Notes, Google_Task_ID]
            all_tasks[notion_id] = test
            print(all_tasks[notion_id])
            #print(data_json['results']['id']['parent']['Task Name', 'Due Date', 'Notes', 'Google Task ID'])


    def get_column_titles(self,data_json):
            return list(data_json["results"][0]["properties"].keys())
            """A function like this would return the properties of the first row of database-> check notion db formating
            it is essentially db with db with db etc etc
            sort of like a multi-dim list but instead databases"""
    def refined_column_titles(self, data_json):
        ref_titles = []
        for e in data_json:
            if e == 'Task Name' or e == 'Due Date' or e == 'Status' or e == 'Google Task ID' or e == 'Notes':
                ref_titles.append(e)
        return ref_titles

    def the_palantir(self):
        """Executes multiple methods and returns a parsed dictionary for each
           tasks sorted off of the google task id"""

        self.tasks_db_json = self.query_database()
        #print(self.tasks_db_json)
        self.column_titles = self.get_column_titles(self.tasks_db_json)

        self.ref_col_titles = self.refined_column_titles(self.column_titles)
        self.retrieve_task_ids(self.tasks_db_json)
        #print(self.ref_col_titles)
        #self.get_all_tasks(self.tasks_db_json)
        #self.task_IDs = self.get_task_id(self.tasks_db_json)
        #print(self.task_IDs)
        #f_task_data = self.get_filtered_task_data(self.tasks_db_json, self.task_titles)
        # trim down db for comparison

    #def copy_all_tasks():
        # This method will be used once to copy all tasks from notion to google tasks

    """
    def get_filtered_task_data(self, tasks_db_json, task_titles):
        task_data = {}
        for title in task_titles:
                if title == "Task Name" and t == "Status" and"""
