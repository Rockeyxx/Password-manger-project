from PyQt5 import QtCore, QtGui, QtWidgets 
from PyQt5.QtWidgets import QMessageBox
from Modules.login import Ui_Login
from Modules.Mainwindow import Ui_MainWindow
from Modules.sqlmodel_manager import SqlModelManager , Catagory , Users , Table_widget
import  os 
import string , random
import sys
import pyperclip , sqlite3 , sqlalchemy
from Modules.encryption import Encryption
    
        

    # def __init__(self):
    #     super().__init__()
    #     app = QtWidgets.QApplication(sys.argv)
    #     self.page()
    #     
    #     sys.exit(app.exec_())




class UIController():

    def page(self):
        self.Login = QtWidgets.QMainWindow()
        self.ui = Ui_Login()
        self.ui.setupUi(self.Login)
        self.Login.show()

        self.mainwindo = QtWidgets.QMainWindow()
        self.mainwindow = Ui_MainWindow()
        self.mainwindow.setupUi(self.mainwindo)
        self.mainwindo.show()

        self.click_btn()

    def generate(self):
        password = []
        for yo in range(3):
            alpha_d = random.choice(string.ascii_letters)
            sym_d = random.choice(string.punctuation)
            num_d = random.choice(string.digits)

            password.append(alpha_d)
            password.append(sym_d)
            password.append(num_d)

        i = "".join(str(x) for x in password)

        self.ui.Password_LineEdit_p2.setText(f"{i}")
        self.ui.ConfirmPassword_LineEdit_p2.setText(f"{i}")
        pyperclip.copy(i)
        self.show_message_box("information" , "Password copied Successfully ")


    def click_btn(self):
        self.ui.pushButton_6.clicked.connect(self.generate)
        self.mainwindow.EditCatagory_btn.clicked.connect(self.edit_catagory)
        self.mainwindow.CopyPassword.clicked.connect(self.copy_password_clicked)
        self.mainwindow.ShowPassword.clicked.connect(self.show_password)

    def edit_catagory(self):
        selected_item = self.mainwindow.treeWidget.selectedItems()

        if selected_item:
            new_text, ok_pressed = QtWidgets.QInputDialog.getText(self.mainwindo, 'Edit Item', 'Edit the category:', text=selected_item[0].text(0))

            if ok_pressed:
                try: 
                 sql = SqlModelManager()
                 sql.update_item(Catagory ,{"username_key": f"{self.ui.Username_LineEdit.text().strip()}" , "catagory": f"{selected_item[0].text(0)}"}, {"catagory": f"{new_text}"})
                 selected_item[0].setText(0, new_text)
                except (sqlite3.IntegrityError , sqlalchemy.exc.IntegrityError):
                    self.show_message_box("Error" , "Cannot name the same Catagory")
                
        else:
            QtWidgets.QMessageBox.warning(self.mainwindo, 'No Item Selected', 'Please select an item to edit.', QtWidgets.QMessageBox.Ok)
    


    def decrypt(self, encrypted_text):
        decrypet = Encryption()
        decrypet.initialize_cipher(self.ui.Password_LineEdit.text())
        return decrypet.decrypt(encrypted_text)

    def copy_password_clicked(self):
        sql = SqlModelManager()

        # Get the selected row in the table
        selected_row = self.mainwindow.tableWidget.currentRow()
        
        if selected_row == -1:
            # Show an error message if no item is selected
            self.show_message_box("Error", "Please select an item.")
            
        else:
        # Get the username_key and catagory from the table
            try:
                # Fetch the password from the SQL model
                data = sql.read(Table_widget)
                # Check if the data exists
                if data:
                    for index ,data1 in enumerate(data):
                      if data1.username_key == self.ui.Username_LineEdit.text().strip() and data1.catagory == self.mainwindow.treeWidget.selectedItems()[0].text(0) and data1.tag_Label == self.mainwindow.tableWidget.item(selected_row, 0).text() and data1.username ==self.mainwindow.tableWidget.item(selected_row, 1).text()  and data1.URL == self.mainwindow.tableWidget.item(selected_row, 3).text():
                        encrypted_password = data1.password
                        # Decrypt the password
                        decrypted_password = self.decrypt(encrypted_password)
                        
                        # Copy the password to the clipboard
                        pyperclip.copy(decrypted_password)
                        self.show_message_box("information" , "Password copied Successfully ")
                else:
                    # Show a message box when no data is found
                    self.show_message_box("Error", "No data found for the selected row.")

            except Exception as e:
                # Show a message box for other exceptions
                self.show_message_box("Error", f"Error fetching password: {e}")
    
    def show_password(self):
        sql = SqlModelManager()
        # Get the selected row in the table
        selected_row = self.mainwindow.tableWidget.currentRow()

        if selected_row == -1:
            # Show an error message if no item is selected
            self.show_message_box("Error", "Please select an item.")
            return


        # Get the username_key and catagory from the table
        
        data = sql.read(Table_widget)
        try:
                if data:

                    for index ,data1 in enumerate(data):
                      if data1.username_key == self.ui.Username_LineEdit.text().strip() and data1.catagory == self.mainwindow.treeWidget.selectedItems()[0].text(0) and data1.tag_Label == self.mainwindow.tableWidget.item(selected_row, 0).text() and data1.username ==self.mainwindow.tableWidget.item(selected_row, 1).text()  and data1.URL == self.mainwindow.tableWidget.item(selected_row, 3).text():
                       
                        if self.mainwindow.tableWidget.item(selected_row,2).text().startswith("•"*len(self.decrypt(data1.password))):
                          # Decrypt the password
                          decrypted_password = self.decrypt(data1.password)
                         
                          # Show the decrypted password in a massage box
                          self.mainwindow.tableWidget.setItem(selected_row , 2 ,QtWidgets.QTableWidgetItem(decrypted_password))
                          break
                        else:
                            self.mainwindow.tableWidget.setItem(selected_row , 2 ,QtWidgets.QTableWidgetItem("•"*len(self.decrypt(data1.password))))
                            break

                        
                else:
                        # Show a message box when no data is found
                        self.show_message_box("Error", "No data found for the selected row.")
                    
        except Exception as e:
                # Show a message box for other exceptions
                self.show_message_box("Error", f"Error decrypting password: {e}")

    def show_message_box(self, title, message):
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec_()

                


        
if __name__ == "__main__":
    x = UIController()
    x.page()


    
   
    


