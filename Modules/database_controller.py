from Modules.encryption import Encryption
import sqlite3 , sqlalchemy
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from Modules.login import Ui_Login 
from Modules.session_controller import SessionController
from Modules.sqlmodel_manager import SqlModelManager , Catagory,Users,Table_widget 
from Modules.EditDialog import EditDialog2
from Modules.Mainwindow import Ui_MainWindow 
from Modules.account_controller import AccountController

  

class DatabaseController(SessionController , AccountController):
    def init(self) :
        self.app = QtWidgets.QApplication(sys.argv)
        self.Login = QtWidgets.QMainWindow()
        self.ui = Ui_Login()
        
        self.mainwindo = QtWidgets.QMainWindow()
        self.mainwindow = Ui_MainWindow()
        self.mainwindow.setupUi(self.mainwindo)
       
        self.ui.setupUi(self.Login)
        self.Login.show()

        self.marwan()
        self.db = SqlModelManager()
        
        sys.exit(self.app.exec_())

    def marwan(self):
        self.setupui()
        self.deleted_items = []
        self.ui.SignUp_btn_p2.clicked.connect(self.signup_page2_button_clicked)
        #--------------------------------------------------------------------------------------------------------------------------------------
        self.mainwindow.EditAccount_btn.clicked.connect(self.editAccount)
        self.mainwindow.DelteAccount_btn.clicked.connect(self.deleteAccount)
        self.mainwindow.Undo.clicked.connect(self.undoAccount)
        self.mainwindow.actionExist.triggered.connect(self.mainwindo.close) # new
        self.mainwindow.actiondelete_the_user.triggered.connect(self.deleteUserAndExit) # new
        self.mainwindow.actionlog_out.triggered.connect(self.returnToLogin) # new
        # undo clicked disable
        self.mainwindow.AddCatgory_btn.clicked.connect(self.disableUndoButton)
        self.mainwindow.EditCatagory_btn.clicked.connect(self.disableUndoButton)
        self.mainwindow.RemoveCatgory_btn.clicked.connect(self.disableUndoButton)
        self.mainwindow.AddAccount_btn.clicked.connect(self.disableUndoButton)
        self.mainwindow.EditAccount_btn.clicked.connect(self.disableUndoButton)
        self.mainwindow.CopyPassword.clicked.connect(self.disableUndoButton)
        self.mainwindow.ShowPassword.clicked.connect(self.disableUndoButton)

    def disableUndoButton(self):
        # Disable the Undo button
        self.mainwindow.Undo.setEnabled(False)
        self.deleted_items = []
#---------------------------------------------------------------------------------------
       
#------------------------------------------------------------------------------------------
        
    def editAccount(self):
        selected_row = self.mainwindow.tableWidget.currentRow()
        self.note = None
        self.private_note = None
        if selected_row != -1:
            sql = SqlModelManager()
            data = sql.read(Table_widget)
            for i , item in enumerate(data): 
                self.tag = self.mainwindow.tableWidget.item(selected_row, 0).text()
                self.username = self.mainwindow.tableWidget.item(selected_row, 1).text()
                self.password = item.password
                self.url = self.mainwindow.tableWidget.item(selected_row, 3).text()
                if self.tag == item.tag_Label and self.username == item.username  and self.url == item.URL and self.ui.Username_LineEdit.text() == item.username_key and self.mainwindow.treeWidget.selectedItems()[0].text(0) == item.catagory:

                    self.note = item.note
                    self.private_note = item.privet_note

            encrypet = Encryption()
            encrypet.initialize_cipher(self.ui.Password_LineEdit.text())
            self.edit_dialog = EditDialog2(self.tag, self.username, encrypet.decrypt(self.password), self.url, self.note , encrypet.decrypt(self.private_note))
            result = self.edit_dialog.exec_()

            if result == QtWidgets.QDialog.Accepted:
                edited_data = self.edit_dialog.getData()

                # Update the table with the edited data
                self.mainwindow.tableWidget.item(selected_row, 0).setText(edited_data['tag'])
                self.mainwindow.tableWidget.item(selected_row, 1).setText(edited_data['username'])
                self.mainwindow.tableWidget.item(selected_row, 2).setText("•"*len(edited_data['password']))
                self.mainwindow.tableWidget.item(selected_row, 3).setText(edited_data['url'])
                

                # Save changes to the database
                self.saveChangesToDatabase()
        else:
            # Show the custom dialog when no row is selected
            self.showNoRowSelectedDialog()
#------------------------------------------------------------------------------
    def showNoRowSelectedDialog(self): # new
        self.msg_box = QtWidgets.QMessageBox()
        self.msg_box.setIcon(QtWidgets.QMessageBox.Information)
        self.msg_box.setText("No Row Selected")
        self.msg_box.setInformativeText("Please select a row before clicking Edit.")
        self.msg_box.setWindowTitle("Information")
        self.msg_box.exec_()
#----------------------------------------------------------------------------------------
    def deleteAccount(self):
     
        selected_row = self.mainwindow.tableWidget.currentRow()
        if selected_row != -1:
            self.undo_data_row = selected_row
            # Save changes to the database
            sql = SqlModelManager()
            data = sql.read(Table_widget)
            self.deleted_item = None 
       
            for index,item in enumerate(data):
                
                
                if item.username_key == self.ui.Username_LineEdit.text().strip() and item.catagory == self.mainwindow.treeWidget.selectedItems()[0].text(0) and item.tag_Label == self.mainwindow.tableWidget.item(selected_row, 0).text() and item.username ==self.mainwindow.tableWidget.item(selected_row, 1).text()  and item.URL == self.mainwindow.tableWidget.item(selected_row, 3).text() :
                 self.deleted_item = item
                 sql.delete_item(Table_widget,ID = F"{item.ID}"
                                 ,username_key=f"{item.username_key}"
                                ,catagory=f"{item.catagory}"
                                ,tag_Label =f"{item.tag_Label}" 
                                ,username = f"{item.username}"
                                ,password= f"{item.password}"
                                ,URL = f"{item.URL}"
                                ,note = f"{item.note}"
                                ,privet_note = f"{item.privet_note}"
                 )
                 # Remove the selected row from the table
            self.mainwindow.tableWidget.removeRow(selected_row)                
            self.mainwindow.Undo.setEnabled(True)
            self.deleted_items.append(self.deleted_item)
    #-------------------------------------------------------------------
    def deleteUserAndExit(self): # new
        message_box = QtWidgets.QMessageBox()
        message_box.setText("all of your data will be deleted if you sure about that press ok (othrwise close this massage)")
        message_box.setWindowTitle("Erorr messege")
        message_box.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Close)

        
        check = message_box.exec_()

        if check == QtWidgets.QMessageBox.Ok:
            sql = SqlModelManager()    
            catagories = sql.read(Catagory)
            table_data = sql.read(Table_widget)
            username_to_delete = self.ui.Username_LineEdit.text()
            sql.delete_item(Users, username=username_to_delete)
            for catagory_data in catagories:
                if catagory_data.username_key == username_to_delete:
                    sql.delete_item(Catagory, username_key=username_to_delete)
            for table_data_row in table_data:
                if table_data_row.username_key == username_to_delete:
                    sql.delete_item(Table_widget, username_key=username_to_delete)
            QtWidgets.QApplication.quit()
        else:
            pass
        
    def returnToLogin(self): # new
        # Close the current window
        self.mainwindo.close()

        # Open the Login window
       
        self.Login.show()
        self.ui.Username_LineEdit.clear()
        self.ui.Password_LineEdit.clear()
    #------------------------------------------------------------------
    def saveChangesToDatabase(self):
        # Save changes to the SQLite database
        edited_data = self.edit_dialog.getData()
        selected_row = self.mainwindow.tableWidget.currentRow()
        for row in range(self.mainwindow.tableWidget.rowCount()):
             QtWidgets.QTableWidgetItem(self.mainwindow.tableWidget.item(row, 0)).text()
             QtWidgets.QTableWidgetItem(self.mainwindow.tableWidget.item(row, 1)).text()
             QtWidgets.QTableWidgetItem(self.mainwindow.tableWidget.item(row, 2)).text()
             QtWidgets.QTableWidgetItem(self.mainwindow.tableWidget.item(row, 3)).text()
             QtWidgets.QTableWidgetItem(self.mainwindow.tableWidget.item(row, 4)).text()
             QtWidgets.QTableWidgetItem(self.mainwindow.tableWidget.item(row, 5)).text()

        sql = SqlModelManager()
        encrypet = Encryption()
        encrypet.initialize_cipher(self.ui.Password_LineEdit.text())
        sql.update_item(Table_widget ,{"username_key": f"{self.ui.Username_LineEdit.text().strip()}" , #search for
                                        "catagory" : f"{self.mainwindow.treeWidget.selectedItems()[0].text(0)}" ,
                                        "tag_Label":f"{self.tag}" , 
                                        "username":f"{self.username}" , 
                                        "password":f"{self.password}" , 
                                        "URL": f"{self.url}",
                                        "note": f"{self.note}",
                                        "privet_note": f"{self.private_note}"
                                        } , #update to
                                        {"tag_Label" : f"{self.mainwindow.tableWidget.item(selected_row, 0).text()}" ,
                                        "username":f"{self.mainwindow.tableWidget.item(selected_row, 1).text()}" ,
                                        "password": f"{encrypet.encrypt(edited_data['password'])}",
                                        "URL": f"{self.mainwindow.tableWidget.item(selected_row, 3).text()}",
                                        "note": f"{edited_data['note']}",
                                        "privet_note": f"{encrypet.encrypt(edited_data['private_note'])}"
                                        }
                                        )
        


        QtWidgets.QMessageBox.information(None, 'Success', 'Changes saved to the database.')
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
        
    def undoAccount(self):
        for deleted_item in self.deleted_items:
      
            sql = SqlModelManager()
            sql.add_item(Table_widget,ID=deleted_item.ID,
                username_key=deleted_item.username_key,
                catagory=deleted_item.catagory,
                tag_Label=deleted_item.tag_Label,
                username=deleted_item.username,
                password=deleted_item.password,
                URL=deleted_item.URL,
                note=deleted_item.note,
                privet_note=deleted_item.privet_note,
            )

            self.update_table()

       
                       
            self.deleted_items = []   
            self.mainwindow.Undo.setEnabled(False)   
            
        
    
    def signup_page2_button_clicked(self):
        #if no user or no password givin
        self.ui.Username_LineEdit.clear()
        self.ui.Password_LineEdit.clear()
        generated_username = self.ui.Username_LineEdit_p2.text().strip()
        generated_password = self.ui.Password_LineEdit_p2.text()
        if ( ( not generated_password)  or (not generated_username) ):
         #msgbox 
            MessegeBox = QtWidgets.QMessageBox()
            MessegeBox.setText("you must enter password and username")
            MessegeBox.setWindowTitle("Erorr messege")
            MessegeBox.exec_() 
        else:
                self.table_input(generated_username)  

    def table_input(self, username):
         if  self.PassWord == self.PassWordConfirm:
            try:
                self.db.add_item(Users ,username=f'{username}' , password=f'{self.DataEncrypation()}')
                self.ui.stackedWidget.setCurrentIndex(0)
                
                
            except sqlalchemy.exc.IntegrityError:
                MessegeBox = QtWidgets.QMessageBox()
                MessegeBox.setText("Username is exist try again")
                MessegeBox.setWindowTitle("Erorr messege")
                MessegeBox.exec_() 
    
    def update_for_tree(self):
        #link with data base
        sql = SqlModelManager()
        data = sql.read(Catagory)
        
        #clear tree before add it 
        self.mainwindow.treeWidget.clear()
        #takes item by item from database
        for items in data :
            #check each item has the same user name
            if items.username_key == self.ui.Username_LineEdit.text().strip():
                    #add catagorys to the tree
                    item = QtWidgets.QTreeWidgetItem(self.mainwindow.treeWidget)
                    item.setText(0 , f"{items.catagory}")
    


if __name__ == '__main__':
    table_instance = DatabaseController()





 



