####################################################################
# @file    : app.py
# @brief   : Register the user details
# @author  : Ganesh Kumar
# @date    : 26 JUL 2019
####################################################################

# Python Global Imports
import os
import sys
from openpyxl import Workbook

# Python Local Imports
import sign_up.sign_up as sign_up
import sign_in.sign_in as sign_in
import sign_out.sign_out as sign_out
import constants.constants as constants
import user_rating.user_rating as user_rating
import database.user_details_database as user_details_database
import database.configure_excel_sheet as configure_excel_sheet

# Python Global Imports
global_total_number_of_booth = 0


def plain_banner_formatting():
    symbol_to_print = '-'
    time_symbol_repeat = 52
    print symbol_to_print * time_symbol_repeat


def format_print(msg):
    symbol_to_print = '~'
    time_symbol_repeat = 52
    new_line = '\n'
    print symbol_to_print * time_symbol_repeat + new_line + msg + new_line + \
          symbol_to_print * time_symbol_repeat


def get_sign_up_inputs_from_user():
    registration_success = False
    while True:
        format_print('Welcome to GK Rating Tracker System - Sign Up Page')
        sign_up_user_name_value = str(
            raw_input('Please Enter your user name: '))
        sign_up_user_original_password_value = str(
            raw_input('Please Enter your password: '))
        sign_up_user_confirmation_password_value = str(
            raw_input('Please Re-Enter your password: '))
        if sign_up_user_name_value is not None and\
                sign_up_user_name_value != '':
            sign_up_object = sign_up.\
                SignUp(sign_up_user_name_value,
                       sign_up_user_original_password_value,
                       sign_up_user_confirmation_password_value)
            if sign_up_object.sign_up_status is True:
                registration_success = True
                get_sign_in_inputs_from_user()
                break
            else:
                print 'Registration Failed, password did not match,' \
                      ' Please try sign up again'
                if registration_success is True:
                    break


def get_sign_in_inputs_from_user():
    while True:
        format_print('Welcome to GK Rating Tracker System - Login Page')
        sign_in_user_name_value = str(raw_input('Please Enter your user '
                                                'name: '))
        sign_in_user_original_password_value = str(raw_input('Please Enter your'
                                                             ' password: '))
        sign_in_object = sign_in.SignIn(sign_in_user_name_value,
                                        sign_in_user_original_password_value)
        if sign_in_object.sign_in_status is True:
            user_rating_object = user_rating.UserRating(sign_in_user_name_value,
                                                        global_total_number_of_booth)
            user_rating_object.get_user_rating()
            if user_rating_object.userRatingStatus is True:
                sign_out_object = sign_out.SignOut()
                break
            else:
                print 'Sign Out Failed'


if __name__ == "__main__":
    database_setup_flag = False
    booth_configuration_setup_flag = False
    while True:
        format_print('Welcome to GK User Rating Tracking System - Home Page')
        tool_options = {1: "SIGN UP",
                        2: "SIGN IN"}
        # print these options
        if database_setup_flag is False:
            print 'setting up the database initiated'
            database_object = user_details_database.DataBaseRead()
            print 'setting up the database completed successfully'
            database_setup_flag = True

        if booth_configuration_setup_flag is False:
            plain_banner_formatting()
            print 'Booth configuration initiated'
            user_rating_excel_file_path = user_details_database.\
                EXCEL_SHEET_FILE_PATH
            # Bring the condition whether user want to configure or not, option
            if not os.path.isfile(user_rating_excel_file_path):
                number_of_booths = int(input('Please Enter the total booth'
                                             ' number to configure the'
                                             ' database: '))
                configure_excel_sheet_status = configure_excel_sheet.\
                    create_user_rating_excel_sheet(number_of_booths)
                if configure_excel_sheet_status is True:
                    print 'Booth Number configuration is completed'
                    constants.TOTAL_BOOTH_NUMBERS_CONFIGURED = number_of_booths
                else:
                    print 'Fail to configure the number of booths to collect' \
                          ' user rating data in the excel sheet, please try' \
                          ' again by deleting the excel sheet if it' \
                          ' gets created'
                    sys.exit(0)
            else:
                print 'tttttttttttttttttt'
                user_rating_excel_file_path = user_details_database. \
                    EXCEL_SHEET_FILE_PATH
                if os.path.isfile(user_rating_excel_file_path):
                    wb_obj = Workbook()
                    sheet_obj = wb_obj.active
                    max_col = sheet_obj.max_column
                    print max_col
                    global_total_number_of_booth = max_col - 1
                    print global_total_number_of_booth
            print 'Booth configuration Completed successfully'
            booth_configuration_setup_flag = True

        plain_banner_formatting()
        for key, value in tool_options.iteritems():
            print key, ':', value
        plain_banner_formatting()

        temp = int(input("Select option you want to proceed: "))
        option_selected = tool_options.get(temp, None).upper().strip()

        if option_selected == 'SIGN UP':
            get_sign_up_inputs_from_user()
        elif option_selected == 'SIGN IN':
            get_sign_in_inputs_from_user()
