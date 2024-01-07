from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import mysql.connector
import MySQLdb
from PyQt5.uic import loadUiType
from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QTableWidget, QVBoxLayout


ui,_ = loadUiType('library_system.ui')

class MainApp(QMainWindow, ui):
	def __init__(self):
		QMainWindow.__init__(self)
		self.setupUi(self)
		self.handle_ui_changes()
		self.handle_buttons()
		self.show_author()
		self.show_category()
		self.show_category_combobox()
		self.show_author_combobox()
		self.show_users()###
		self.search_user()
		self.edit_dialog = None


		self.pushButton_15.clicked.connect(self.search_user)
  		#Initializing the edit dialog as a class attribute

		
	def handle_ui_changes(self):
		self.tabWidget.tabBar().setVisible(False)

	def handle_buttons(self):
		self.pushButton.clicked.connect(self.open_day_to_day_tab)
		self.pushButton_2.clicked.connect(self.open_books_tab)
		self.pushButton_3.clicked.connect(self.open_users_tab)
		self.pushButton_4.clicked.connect(self.open_settings_tab)
		self.pushButton_10.clicked.connect(self.add_new_user)
		self.pushButton_12.clicked.connect(self.edit_user_data)
		self.pushButton_7.clicked.connect(self.add_book)
		self.pushButton_13.clicked.connect(self.add_category) ###?
		self.pushButton_14.clicked.connect(self.add_author) 
		#self.pushButton_15.clicked.connect(self.search_user)

 

########### opening tabs #################

	def open_day_to_day_tab(self):
		self.tabWidget.setCurrentIndex(0)

	def open_books_tab(self):
		self.tabWidget.setCurrentIndex(1)


	def open_users_tab(self):
		self.tabWidget.setCurrentIndex(2)


	def open_settings_tab(self):
		self.tabWidget.setCurrentIndex(3)

########### books #################

	def add_book (self):
		self.db= MySQLdb.connect(host='localhost',user='lms_user',password='Lmspassword!?',db='library')
		self.cur=self.db.cursor()

		book_title=self.lineEdit_2.text()
		book_code=self.lineEdit_3.text()
		book_category=self.comboBox_3.currentText()
		book_author=self.comboBox_4.currentText()

		

	def search_book(self):
		self.tabWidget.setCurrentIndex(1)


	def edit_book(self):
		self.tabWidget.setCurrentIndex(2)


	def delete_boook(self):
		self.tabWidget.setCurrentIndex(3)

########### user #################

	def show_users(self):
		self.db = MySQLdb.connect(host='localhost', user='lms_user', password='Lmspassword!?', db='library')
		self.cur = self.db.cursor()
		self.cur.execute('''SELECT user_name,user_email, user_password FROM users''')
		data = self.cur.fetchall()

		if data:
			self.tableWidget_5.setRowCount(0)
			self.tableWidget_5.insertRow(0)
			for row, form in enumerate(data):
				for column, item in enumerate(form):
					self.tableWidget_5.setItem(row, column, QTableWidgetItem(str(item)))
					column += 1
				row_position = self.tableWidget_5.rowCount()
				self.tableWidget_5.insertRow(row_position)

	def add_new_user(self):
		self.db = MySQLdb.connect(host='localhost', user='lms_user', password='Lmspassword!?', db='library')
		self.cur = self.db.cursor()

		user_name = self.lineEdit_6.text()
		email = self.lineEdit_8.text()
		password = self.lineEdit_7.text()

		self.cur.execute('''
			INSERT INTO users (user_name, user_email, user_password) VALUES (%s, %s, %s)
			''', (user_name, email, password))

		self.db.commit()
		self.statusBar().showMessage('New User Added')
		print('done')

		self.lineEdit_6.setText('')
		self.lineEdit_8.setText('')
		self.lineEdit_7.setText('')

		self.show_users()


	def show_user_details(self, item):
		user_name=self.tableWidget_5.item(item.row(),0).text()
		user_email=self.tableWidget_5.item(item.row(),1).text()
		# Retrieve user details based on the selected item and display them


	def edit_user_data(self):
	    selected_user_row = self.tableWidget_5.currentRow()

	    if selected_user_row >= 0:
	        selected_user_name = self.tableWidget_5.item(selected_user_row, 0).text()

	        # Retrieve additional user data as needed
	        # For example, you might perform a database query to get user details

	        # Open a simple dialog for editing
	        edit_dialog = QDialog(self)
	        edit_dialog.setWindowTitle("Edit User Data")

	        # Add widgets to edit_dialog for editing user data
	        edit_layout = QVBoxLayout(edit_dialog)
	        edit_layout.addWidget(QLabel(f"Editing data for user: {selected_user_name}"))

	        # Add input fields for editing user data
	        new_name_label = QLabel("New Name:")
	        new_name_edit = QLineEdit()
	        edit_layout.addWidget(new_name_label)
	        edit_layout.addWidget(new_name_edit)

	        new_email_label = QLabel("New Email:")
	        new_email_edit = QLineEdit()
	        edit_layout.addWidget(new_email_label)
	        edit_layout.addWidget(new_email_edit)

	        #Save changes button
	        save_button = QPushButton("Save Changes")
	        save_button.clicked.connect(lambda: self.save_user_changes(selected_user_name, new_name_edit.text(), new_email_edit.text()))
	        edit_layout.addWidget(save_button)

	        edit_dialog.exec_()
	    else:
	        # Handle the case where no user is selected
	        QMessageBox.warning(self, "No User Selected", "Please select a user to edit.")


	def save_user_changes(self, user_name, new_name, new_email):
	#save changes to the database
		try:
			self.db = MySQLdb.connect(host='localhost', user='lms_user', password='Lmspassword!?', db='library')
			self.cur = self.db.cursor()

			# Example: Use an UPDATE query to modify the user's data
			self.cur.execute("UPDATE users SET user_name = %s, user_email = %s WHERE user_name = %s", (new_name, new_email, user_name))

			self.db.commit()
			self.statusBar().showMessage('User data updated successfully')
			print('User data updated successfully')

		except Exception as e:
			# Handle exceptions, log errors, and display error messages 
			print(f"Error updating user data: {e}")
			self.statusBar().showMessage('Error updating user data')

		finally:
			# Close the database connection
			self.db.close()

		# After saving changes, refresh the user list
		self.show_users()
		self.sender().parent().accept()  # Close the dialog




				# Add this method in your MainApp class
	def search_user(self):
	    search_name = self.lineEdit_9.text()
	    search_email = self.lineEdit_10.text()
	    search_password = self.lineEdit_11.text()

	    # Create the SQL query based on the provided search criteria
	    conditions = []
	    if search_name:
	        conditions.append(f"user_name LIKE '%{search_name}%'")

	    if search_email:
	        conditions.append(f"user_email LIKE '%{search_email}%'")

	    if search_password:
	        conditions.append(f"user_password LIKE '%{search_password}%'")

	    # Combine conditions with AND if there are multiple
	    query = "SELECT * FROM users"
	    if conditions:
	        query += " WHERE " + " AND ".join(conditions)

	    # Execute the query and update the user table
	    self.cur.execute(query)
	    data = self.cur.fetchall()

	    if data:
	        self.tableWidget_5.setRowCount(0)
	        for row, form in enumerate(data):
	            self.tableWidget_5.insertRow(row)
	            for column, item in enumerate(form):
	                self.tableWidget_5.setItem(row, column, QTableWidgetItem(str(item)))

	    # If no results are found, you can display a message
	    if not data:
	        self.statusBar().showMessage('No matching users found.')


	# Connect the button to the search_user method



########### categories #################


	def add_category(self):
		self.db= MySQLdb.connect(host='localhost',user='lms_user',password='Lmspassword!?',db='library')
		self.cur=self.db.cursor()

		category_name=self.lineEdit_16.text()

		self.cur.execute('''
			INSERT INTO category (category_name)VALUES(%s)
			''',(category_name,))

		self.db.commit()
		self.statusBar().showMessage('New Category Added')
		print('done')

		self.lineEdit_16.setText('')

		self.show_category()

	def show_category(self):
		self.db= MySQLdb.connect(host='localhost',user='lms_user',password='Lmspassword!?',db='library')
		self.cur=self.db.cursor()

		self.cur.execute('''SELECT category_name FROM category''')
		data= self.cur.fetchall()

		print(data)
		if data:
			self.tableWidget_2.setRowCount(0)
			self.tableWidget_2.insertRow(0)
			for row, form in enumerate(data):
				for column, item in enumerate(form):
					self.tableWidget_2.setItem(row,column,QTableWidgetItem(str(item)))
					column+=1
				row_position= self.tableWidget_2.rowCount()
				self.tableWidget_2.insertRow(row_position)


	def add_author(self):
		self.db= MySQLdb.connect(host='localhost',user='lms_user',password='Lmspassword!?',db='library')
		self.cur=self.db.cursor()

		author_name=self.lineEdit_17.text()

		self.cur.execute('''
			INSERT INTO author (author_name)VALUES(%s)
			''',(author_name,))

		self.db.commit()
		self.lineEdit_17.setText('') # check
		self.statusBar().showMessage('New Author Added')
		print('done')
		self.show_author()


	def show_author(self):
		self.db= MySQLdb.connect(host='localhost',user='lms_user',password='Lmspassword!?',db='library')
		self.cur=self.db.cursor()

		self.cur.execute('''SELECT author_name FROM author''')
		data= self.cur.fetchall()

		if data:
			self.tableWidget_3.setRowCount(0)
			self.tableWidget_3.insertRow(0)
			for row, form in enumerate(data):
				for column, item in enumerate(form):
					self.tableWidget_3.setItem(row,column,QTableWidgetItem(str(item)))
					column+=1
				row_position= self.tableWidget_3.rowCount()
				self.tableWidget_3.insertRow(row_position)


########### show settings data in UI #################

	def show_category_combobox(self):
		self.db= MySQLdb.connect(host='localhost',user='lms_user',password='Lmspassword!?',db='library')
		self.cur=self.db.cursor()

		self.cur.execute('''SELECT category_name FROM category''')
		data=self.cur.fetchall()

		print(data)

		for category in data:
			self.comboBox_3.addItem(category[0])



	def show_author_combobox(self): #combobox misspelled?
		self.db= MySQLdb.connect(host='localhost',user='lms_user',password='Lmspassword!?',db='library')
		self.cur=self.db.cursor()

		self.cur.execute('''SELECT author_name FROM author''')
		data=self.cur.fetchall()
		for author in data:
			self.comboBox_4.addItem(author[0])

def main():
	app=QApplication(sys.argv)
	window=MainApp()
	window.show()
	app.exec_()


if __name__ == '__main__':
	main()
























