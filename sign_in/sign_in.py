####################################################################
# @file    : sing_in.py
# @brief   : sign into the user account, only one user can sign into
#            the account at a time
# @author  : Ganesh Kumar
# @date    : 8 AUG 2019
####################################################################

# Python Local Imports
import database.user_details_database as user_details_database


class SignIn(object):
    sign_in_status = False

    def __init__(self, sign_in_user_name, sign_in_password):
        self.sign_in_user_name = sign_in_user_name
        self.sign_in_password = sign_in_password
        self.sign_in_authentication_verification_call()

    def sign_in_authentication_verification_call(self):
        sign_in_authentication_check_status = self.sign_in_authentication_check\
            (str(self.sign_in_user_name), str(self.sign_in_password))
        if sign_in_authentication_check_status is True:
            self.sign_in_status = True
            print 'User logged in Success'
        else:
            pass

    @staticmethod
    def sign_in_authentication_check(sign_in_user_name, sign_in_password):
        user_login_time_password = user_details_database.USER_DETAILS_DICT.\
            get(sign_in_user_name, None)
        if user_login_time_password is not None:
            if sign_in_password == user_login_time_password:
                return True
            else:
                print 'Password Incorrect'
                return False
        else:
            print 'User name does not exists/Incorrect,' \
                  ' please check and try again'
            return False
