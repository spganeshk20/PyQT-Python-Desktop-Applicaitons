####################################################################
# @file    : user_details_database.py
# @brief   : Maintains the user sign in details
# @author  : Ganesh Kumar
# @date    : 8 AUG 2019
####################################################################
# Python Global Imports
import os
import json

# Global Constants
USER_DETAILS_DICT = dict()
STR_FILE_NAME_USER_DETAILS_DICT = 'user_details_dict.json'
STR_FILE_NAME_USER_DETAILS_EXCEL_SHEET = 'user_data_sheet.xlsx'
DATABASE_JSON_FILE_PATH = 'database' + os.sep + 'user_details_json_db' + \
                          os.sep + STR_FILE_NAME_USER_DETAILS_DICT
EXCEL_SHEET_FILE_PATH = 'database' + os.sep + 'user_data_collector_excel_db'\
                        + os.sep + STR_FILE_NAME_USER_DETAILS_EXCEL_SHEET


class DataBaseRead(object):
    def __init__(self):
        self.database_read()

    @staticmethod
    def database_update():
        with open(DATABASE_JSON_FILE_PATH, 'w+') as file_obj:
            file_obj.truncate()
            file_obj.seek(0)
            dict_to_json_data = json.dump(USER_DETAILS_DICT)
            file_obj.write(dict_to_json_data)

    @staticmethod
    def database_read():
        try:
            global USER_DETAILS_DICT
            if os.path.exists(DATABASE_JSON_FILE_PATH):
                with open(DATABASE_JSON_FILE_PATH, 'r') as file_obj:
                        USER_DETAILS_DICT = json.load(file_obj)
            else:
                print 'Database does not exists'
        except ValueError:
            print 'here'
            pass
