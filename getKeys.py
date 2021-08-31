import json
import ast
from keyPath import PATH as PATH


def get_Keys():
    with open(PATH) as f:
        data = json.load(f)
        parsed_data = ast.literal_eval(data)
        print("***SECRET***")
        #print(data)
        #print(parsed_data)
        NOTION_DATABASE_ID = parsed_data['NOTION_DATABASE_ID']
        NOTION_INTEGRATION_TOKEN = parsed_data["NOTION_INTEGRATION_TOKEN"]
        GOOGLE_TO_DO_DAILY_TASKLIST_ID= parsed_data["GOOGLE_TO_DO_DAILY_TASKLIST_ID"]
        return(parsed_data)
        #print(NOTION_DATABASE_ID)
        #print(NOTION_INTEGRATION_TOKEN)
        #print(GOOGLE_TO_DO_DAILY_TASKLIST_ID)

def set_Keys(dictionary_of_keys):
    keys_dict = dictionary_of_keys
    print(keys_dict)
    secret_keys_json = json.dumps(keys_dict)
    with open('secret_keys.json', 'w') as json_file:
        json.dump(secret_keys_json, json_file)

def convert_to_RFC_datetime(year=1900, month=1, day=1, hour=0, minute=0):
    dt = datetime.datetime(year, month, day, hour, minute, 0, 000).isoformat() + 'Z'
    return dt

#set_Keys({"NOTION_DATABASE_ID" : "", "NOTION_INTEGRATION_TOKEN" : "", "GOOGLE_TO_DO_DAILY_TASKLIST_ID" : ""})
#get_Keys()
