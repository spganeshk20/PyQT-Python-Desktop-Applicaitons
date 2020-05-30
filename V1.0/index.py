from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
import sqlite3
import sys
import os
from xlrd import *
from xlsxwriter import *


from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import random

current_directory = os.getcwd()
# database_path = str(current_directory + os.sep + 'database' + os.sep + 'my_database.db')
database_path = r'C:\sqlite\my_database.db'

ui, _ = loadUiType('registration.ui')

about_screen = 0
help_screen = 1
sign_up_screen = 2
login_screen = 3
admin_login_screen = 4
admin_control_screen = 5
user_rating_screen = 6
rating_analysis_screen = 7
add_delete_admin_users_screen = 8


class MainApp(QMainWindow, ui):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.login_username = None
        self.booth_name = None
        self.user_rating_value = None
        self.login_password = None
        self.title = 'Booth Rating Tracking and Report Generation System'
        self.handle_ui_changes()
        self.handle_ui_buttons()
        # self.plot_chart_db()

    def handle_ui_changes(self):
        self.setWindowTitle(self.title)
        self.hide_theme_bar()
        self.tabWidget.tabBar().setVisible(False)
        self.about_button.setToolTip('About')
        self.help_button.setToolTip('Help')
        self.login_button.setToolTip('User Login')
        self.sign_up_button.setToolTip('User Sign Up')
        self.admin_button.setToolTip('Admin Login')
        self.theme_button.setToolTip('Themes')
        self.dark_orange_theme()

    def handle_ui_buttons(self):
        self.theme_bar_hide_button.clicked.connect(self.hide_theme_bar)
        self.theme_button.clicked.connect(self.show_themes_bar)

        self.about_button.clicked.connect(self.about_tab)
        self.help_button.clicked.connect(self.help_tab)
        self.login_button.clicked.connect(self.login_tab)
        self.sign_up_button.clicked.connect(self.sign_up_tab)
        self.admin_button.clicked.connect(self.admin_tab)

        self.login_success_button.clicked.connect(self.user_rating_event)
        self.rating_analysis_button.clicked.connect(self.reporting)
        self.admin_login_succes.clicked.connect(self.admin_controls)
        self.sign_up_success_button.clicked.connect(self.push_sign_up_user_data_to_db)

        self.add_admin_users_button.clicked.connect(self.add_admin_users_tab)
        self.admin_add_user_button.clicked.connect(self.add_admin_data_to_db)

        self.delete_admin_users_button.clicked.connect(self.delete_admin_users_tab)
        self.admin_delete_user_button.clicked.connect(self.delete_admin_data_to_db)

        self.admin_add_user_delete_page_back_button.clicked.connect(self.admin_controls)

        self.admin_log_out_button.clicked.connect(self.admin_tab)
        self.user_log_out_button.clicked.connect(self.login_tab)
        self.user_rating_back_button.clicked.connect(self.admin_controls)

        self.user_rating_data_submit_button.clicked.connect(self.submit_data_to_db)
        self.export_final_report_button.clicked.connect(self.export_report_in_excel)

        ############Themes Button###############
        self.dark_blue_theme_button.clicked.connect(self.dark_blue_theme)
        self.dark_orange_theme_button.clicked.connect(self.dark_orange_theme)
        self.dark_theme_button.clicked.connect(self.dark_theme)
        self.dark_gray_theme_button.clicked.connect(self.dark_gray_theme)

    def show_themes_bar(self):
        self.theme_group_box.show()

    def hide_theme_bar(self):
        self.theme_group_box.hide()
        
    def about_tab(self):
        self.tabWidget.setCurrentIndex(about_screen)

    def help_tab(self):
        self.tabWidget.setCurrentIndex(help_screen)

    def sign_up_tab(self):
        self.tabWidget.setCurrentIndex(sign_up_screen)
        self.sign_up_faiure_msg_label.clear()
        self.sign_up_user_name_line_edit.clear()
        self.sign_up_password_line_edit.clear()
        self.sign_up_confirm_password_line_edit.clear()

    def push_sign_up_user_data_to_db(self):
        self.username = self.sign_up_user_name_line_edit.text()
        self.password = self.sign_up_password_line_edit.text()
        self.confirm_password = self.sign_up_confirm_password_line_edit.text()

        if self.password != '' and self.confirm_password != '':
            if self.confirm_password == self.password:
                db = sqlite3.connect(database_path)
                cur = db.cursor()
                insert_query = """INSERT INTO 'users_table' ('username', 'password')
                         VALUES (?, ?);"""
                data_tuple = (str(self.username), str(self.password))
                cur.execute(insert_query, data_tuple)
                db.commit()
                cur.close()
                self.statusBar().showMessage('Signed Up successful')
                self.tabWidget.setCurrentIndex(login_screen)

                self.sign_up_user_name_line_edit.clear()
                self.sign_up_password_line_edit.clear()
                self.sign_up_confirm_password_line_edit.clear()
            else:
                self.sign_up_faiure_msg_label.setText('Password Mismatch')
                self.tabWidget.setCurrentIndex(sign_up_screen)
        else:
            self.sign_up_faiure_msg_label.setText('Field User Name or Password is empty')
            self.tabWidget.setCurrentIndex(sign_up_screen)

    def login_tab(self):
        self.login_failure_msg_label.clear()
        self.statusBar().clearMessage()
        self.tabWidget.setCurrentIndex(login_screen)

    def user_rating_event(self):
        self.login_username = self.login_user_name_line_edit.text()
        self.login_password = self.login_password_line_edit.text()

        # Read the DB and compare the username and password and login
        if self.login_username != '' and self.login_password != '':
            db = sqlite3.connect(database_path)
            cur = db.cursor()
            read_query = """SELECT * FROM 'users_table';"""
            cur.execute(read_query)
            data = cur.fetchall()

            for value in data:
                if self.login_username == value[0]:
                    if self.login_password == value[1]:
                        self.statusBar().showMessage('Logged in successfully')
                        self.tabWidget.setCurrentIndex(user_rating_screen)
                        break
                    else:
                        self.login_failure_msg_label.setText('Invalid User Name and Password')
                        self.tabWidget.setCurrentIndex(login_screen)
                else:
                    self.login_failure_msg_label.setText('User does not exists, please sign up')
                    self.tabWidget.setCurrentIndex(login_screen)
            self.login_user_name_line_edit.clear()
            self.login_password_line_edit.clear()
        else:
            self.login_failure_msg_label.setText('Field User Name or Password is empty')
            self.tabWidget.setCurrentIndex(login_screen)

        self.user_rating_value = self.comboBox.currentText()
        self.booth_name = self.comboBox_2.currentText()

    def admin_tab(self):
        self.tabWidget.setCurrentIndex(admin_login_screen)
        self.admin_user_name_line_edit.clear()
        self.admin_password_line_edit.clear()
        self.admin_login_failure_msg_label.clear()

    def admin_controls(self):
        self.admin_login_username = self.admin_user_name_line_edit.text()
        self.admin_login_password = self.admin_password_line_edit.text()

        # Read the DB and compare the username and password and login
        if self.admin_login_username != '' and self.admin_login_password != '':
            db = sqlite3.connect(database_path)
            cur = db.cursor()
            read_query = """SELECT * FROM 'admin_users_table';"""
            cur.execute(read_query)
            data = cur.fetchall()

            for value in data:
                if self.admin_login_username == value[0] and self.admin_login_password == value[1]:
                    self.statusBar().showMessage('Admin Logged in successfully')
                    self.tabWidget.setCurrentIndex(admin_control_screen)
                    break
                else:
                    self.admin_login_failure_msg_label.setText('Invalid User Name and Password')
            self.login_user_name_line_edit.clear()
            self.login_password_line_edit.clear()
        else:
            self.admin_login_failure_msg_label.setText('Field User Name or Password is empty')

    def add_admin_users_tab(self):
        self.tabWidget.setCurrentIndex(add_delete_admin_users_screen)
        self.add_admin_user_group_box.setEnabled(True)
        self.delete_admin_user_group_box.setEnabled(False)
        self.add_admin_user_name_line_edit.clear()
        self.add_admin_password_line_edit.clear()
        self.add_admin_confirm_password_line_edit.clear()
        self.add_admin_user_msg.clear()
        self.delete_admin_user_msg.clear()

    def add_admin_data_to_db(self):
        self.admin_user_name_to_add = self.add_admin_user_name_line_edit.text()
        self.admin_password_to_add = self.add_admin_password_line_edit.text()
        self.admin_confirm_password_to_add = self.add_admin_confirm_password_line_edit.text()

        if self.admin_user_name_to_add != '' and self.admin_password_to_add != '':
            if self.admin_confirm_password_to_add == self.admin_password_to_add:
                db = sqlite3.connect(database_path)
                cur = db.cursor()
                insert_query = """INSERT INTO 'admin_users_table' ('admin_user_name', 'admin_password')
                         VALUES (?, ?);"""
                data_tuple = (str(self.admin_user_name_to_add), str(self.admin_password_to_add))
                cur.execute(insert_query, data_tuple)
                db.commit()
                cur.close()

                self.add_admin_user_name_line_edit.clear()
                self.add_admin_password_line_edit.clear()
                self.add_admin_confirm_password_line_edit.clear()

                self.statusBar().showMessage('Admin User added successfully')
                self.add_admin_user_msg.setText('Admin User added Successfully')
                self.tabWidget.setCurrentIndex(admin_control_screen)
            else:
                self.add_admin_user_msg.setText('Password Mismatch')
        else:
            self.add_admin_user_msg.setText('User or Password is empty')

    def delete_admin_users_tab(self):
        self.tabWidget.setCurrentIndex(add_delete_admin_users_screen)
        self.add_admin_user_group_box.setEnabled(False)
        self.delete_admin_user_group_box.setEnabled(True)
        self.delete_admin_user_name_line_edit.clear()
        self.delete_admin_user_msg.clear()
        self.add_admin_user_msg.clear()

    def delete_admin_data_to_db(self):
        self.to_delete_admin_user_name = self.delete_admin_user_name_line_edit.text()

        if self.to_delete_admin_user_name != '':
            db = sqlite3.connect(database_path)
            cur = db.cursor()
            read_query = """SELECT * FROM 'admin_users_table';"""
            cur.execute(read_query)
            data = cur.fetchall()

            for value in data:
                if self.to_delete_admin_user_name == value[0]:
                    delete_query = "DELETE from admin_users_table where admin_user_name = '%s'" % self.to_delete_admin_user_name
                    cur.execute(delete_query)
                    db.commit()
                    cur.close()
                    self.statusBar().showMessage('Admin User Name Removed successfully')
                    self.tabWidget.setCurrentIndex(admin_control_screen)
                    break
                else:
                    self.delete_admin_user_msg.setText('User Name does not exists')
            self.delete_admin_user_name_line_edit.clear()
        else:
            self.delete_admin_user_msg.setText('Field User name is empty')

    def reporting(self):
        self.tabWidget.setCurrentIndex(rating_analysis_screen)
        self.plot_chart_db()
        # Rating analysis code
        db = sqlite3.connect(database_path)
        cur = db.cursor()
        read_query = """SELECT * FROM 'user_rating_table';"""
        cur.execute(read_query)
        data = cur.fetchall()

        if data is not None:
            self.tableWidget.setRowCount(0)
            for row, form in enumerate(data):
                row_position = self.tableWidget.rowCount()
                self.tableWidget.insertRow(row_position)
                for column, value in enumerate(form):
                    self.tableWidget.setItem(row, column, QTableWidgetItem(value))
                    column += 1
        cur.close()

    def submit_data_to_db(self):
        db = sqlite3.connect(database_path)
        cur = db.cursor()
        insert_query = """INSERT INTO 'user_rating_table' ('username', 'user_rating', 'booth_number')
         VALUES (?, ?, ?);"""
        data_tuple = (str(self.login_username), str(self.user_rating_value), str(self.booth_name))
        cur.execute(insert_query, data_tuple)
        db.commit()
        cur.close()
        self.statusBar().showMessage('Rating logged successfully')
        self.login_tab()

    def export_report_in_excel(self):
        db = sqlite3.connect(database_path)
        cur = db.cursor()
        read_query = """SELECT * FROM 'user_rating_table';"""
        cur.execute(read_query)
        data = cur.fetchall()

        wb = Workbook('user_rating_report.xlsx')
        sheet1 = wb.add_worksheet()

        sheet1.write(0, 0, 'User Name')
        sheet1.write(0, 1, 'Booth Name')
        sheet1.write(0, 2, 'User Rating')

        row_number = 1
        for row in data:
            column_number = 0
            for item in row:
                sheet1.write(row_number, column_number, str(item))
                column_number += 1
            row_number += 1

        wb.close()
        self.statusBar().showMessage('User Rating Report xlsx Downloaded Successfully')


    def dark_blue_theme(self):
        style = open('themes\\dark_blue.css', 'r')
        style = style.read()
        self.setStyleSheet(style)

    def dark_orange_theme(self):
        style = open('themes\\dark_orange.css', 'r')
        style = style.read()
        self.setStyleSheet(style)

    def dark_theme(self):
        style = open('themes\\dark.css', 'r')
        style = style.read()
        self.setStyleSheet(style)

    def dark_gray_theme(self):
        style = open('themes\\dark_gray.css', 'r')
        style = style.read()
        self.setStyleSheet(style)

    def plot_chart_db(self):
        m = PlotCanvas(self, width=5, height=4)
        m.move(500, 100)


class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.plot()

    def plot(self):
        data = [random.random() for i in range(25)]
        ax = self.figure.add_subplot(111)
        ax.plot(data, 'r-')
        ax.set_title('PyQt Matplotlib Example')
        self.draw()


def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()