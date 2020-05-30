####################################################################
# @file    : sign_up.py
# @brief   : creates new user account
# @author  : Ganesh Kumar
# @date    : 8 AUG 2019
####################################################################

# Python Global Imports
import os
import sys
import json

# Python Local Imports
import constants.constants as constants
import database.user_details_database as user_details_database


class SignUp(object):
    sign_up_status = False

    def __init__(self, sign_up_user_name, sign_up_original_password,
                 sign_up_confirmation_password):
        self.sign_up_user_name = sign_up_user_name
        self.sign_up_original_password = sign_up_original_password
        self.sign_up_confirmation_password = sign_up_confirmation_password
        self.password_authentication_during_sign_up()

    def password_authentication_during_sign_up(self):
        user_name_existence_check_status = \
            self.user_name_existence_check_during_sign_up(self.sign_up_user_name)
        if user_name_existence_check_status is True:
            sign_up_password_verification_status = self.\
                sign_up_original_and_confirm_password_verification\
                (self.sign_up_original_password,
                 self.sign_up_confirmation_password)
            if sign_up_password_verification_status is True:
                # Store the user name and password
                user_details_database.USER_DETAILS_DICT[self.sign_up_user_name]\
                    = self.sign_up_confirmation_password
                self.sign_up_status = True
                self.update_user_details_dictionary\
                    (self.sign_up_user_name, self.sign_up_confirmation_password)
                print 'Registration Success for the user - %s' % self.\
                    sign_up_user_name
                self.sign_up_database_update()
            else:
                pass
        else:
            print 'User name already exists, please try login'
            sys.exit(0)

    @staticmethod
    def update_user_details_dictionary(key, value):
        user_details_database.USER_DETAILS_DICT[key] = value

    @staticmethod
    def user_name_existence_check_during_sign_up(sign_up_user_name):
        user_name_existence_check_value = user_details_database.\
            USER_DETAILS_DICT.get(sign_up_user_name, None)
        if user_name_existence_check_value is None:
            return True
        else:
            return False

    @staticmethod
    def sign_up_original_and_confirm_password_verification\
                    (sign_up_original_password, sign_up_confirmation_password):
        if sign_up_confirmation_password == sign_up_original_password:
            return True
        else:
            return False

    @staticmethod
    def sign_up_database_update():
        with open(user_details_database.DATABASE_JSON_FILE_PATH, 'w+')\
                as file_obj:
            file_obj.truncate()
            file_obj.seek(0)
            dict_to_json_data = json.dumps(user_details_database.
                                           USER_DETAILS_DICT, indent=4)
            file_obj.write(dict_to_json_data)

