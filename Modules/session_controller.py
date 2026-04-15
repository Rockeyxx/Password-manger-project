#Bilal Hassan - 2136347
from Modules.encryption import Encryption
from cryptography.fernet import Fernet
import sys
from PyQt5 import  QtWidgets
from Modules.login import Ui_Login 
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton
from Modules.Mainwindow import Ui_MainWindow
from Modules.sqlmodel_manager import SqlModelManager,Catagory,Table_widget
from Modules.account_controller import AccountController


class SessionController(Encryption , AccountController):
    def init(self):
         super().__init__()
         self.app = QtWidgets.QApplication(sys.argv)
         self.Login = QtWidgets.QMainWindow()
         self.ui = Ui_Login()
         self.ui.setupUi(self.Login)
         self.setupui()
         self.mainwindo = QtWidgets.QMainWindow()
         self.mainwindow = Ui_MainWindow()
         self.mainwindow.setupUi(self.mainwindo)
         self.setupui()
         self.database = SqlModelManager()
         sys.exit(self.app.exec_())
    
    def setupui(self):
        self.ui.SignUp_btn_p2.clicked.connect(self.DataEncrypation)
        self.mainwindow.RemoveCatgory_btn.clicked.connect(self.RemoveCatagory)
        self.mainwindow.AddAccount_btn.clicked.connect(self.addAccound)

    def DataCheck(self):
        self.PassWord = self.ui.Password_LineEdit_p2.text()
        self.PassWordConfirm = self.ui.ConfirmPassword_LineEdit_p2.text()
        if  self.PassWord == self.PassWordConfirm:
        
            return True
        else:
  
            MessegeBox = QtWidgets.QMessageBox()
            MessegeBox.setText("Enter The Same Password")
            MessegeBox.setWindowTitle("Erorr messege")
            
            MessegeBox.exec_()

            return False
                
    def DataEncrypation(self):# the method that contian encrypted password
        if self.DataCheck():
            self.initialize_cipher(str(self.PassWord))
            SecretPassWord = self.encrypt(str(self.PassWord))
            return SecretPassWord
        
    def NonExitRecordEM(self):
        MessegeBox = QtWidgets.QMessageBox()
        MessegeBox.setText("please choose an item")
        MessegeBox.setWindowTitle("Erorr messege")
        MessegeBox.exec_()

    def DeleteCatagoryM(self,item = "item"):
        MessegeBox = QtWidgets.QMessageBox()
        MessegeBox.setText(f"the catagory '{item}' have been deleted")
        MessegeBox.setWindowTitle("Action messege")
        MessegeBox.exec_()

        
    def RemoveCatagory(self):#check if the record exited in the catagory
            if not self.mainwindow.treeWidget.selectedItems():
                self.NonExitRecordEM()
            else: 
                sql = SqlModelManager()
                database_items = sql.read(Catagory)
                #take the selected items
                for items in self.mainwindow.treeWidget.selectedItems():
                    catagory_value = items.text(0)
                    username_key_value = self.ui.Username_LineEdit.text().strip()  
                    #check if the value is the same in database to delete it
                    for catagory_instance in database_items:
                        if catagory_value == catagory_instance.catagory and username_key_value == catagory_instance.username_key:
                            sql.delete_item(Catagory , username_key=f"{username_key_value}", catagory= f"{catagory_value}")
                            sql.delete_item(Table_widget ,username_key=f"{username_key_value}", catagory= f"{catagory_value}")
                            self.DeleteCatagoryM(catagory_value)
                            self.mainwindow.treeWidget.takeTopLevelItem(self.mainwindow.treeWidget.indexOfTopLevelItem(items))
                            break
                    else: 
                            #if this ooucuered somthing wrong in other codes 
                            MessegeBox = QtWidgets.QMessageBox()
                            MessegeBox.setText(F"the catagory {items.text(0)} Dosent exsit in data base")
                            MessegeBox.setWindowTitle("Erorr massage")
                            MessegeBox.exec_()

    def addAccound(self):
       try:
        self.mainwindow.treeWidget.selectedItems()[0].text(0)   
        self.dialog = QDialog()
        self.dialog.setWindowTitle("Add accound data")
        self.dialog.setFixedSize(500,450)
        # Layout
        layout = QVBoxLayout()

        # Line Edits
        self.Tag = QLineEdit()
        self.Username = QLineEdit()
        self.Password = QLineEdit()
        self.URL = QLineEdit()
        self.Note = QLineEdit()
        self.PrivateNote = QLineEdit()


        # Labels
        self.TagLabel = QLabel("Enter tag:")
        self.UsernameLabel = QLabel("Enter username:")
        self.PassowordLabel = QLabel("Enter password:")
        self.URLLabel = QLabel("Enter URL:")
        self.NoteLabel = QLabel("Enter note:")
        self.PrivateNoteLabel = QLabel("Enter private note:")


        # Add widgets to layout
        layout.addWidget(self.TagLabel)
        layout.addWidget(self.Tag)

        layout.addWidget(self.UsernameLabel)
        layout.addWidget(self.Username)

        layout.addWidget( self.PassowordLabel)
        layout.addWidget(self.Password)

        layout.addWidget(self.URLLabel)
        layout.addWidget(self.URL)
        
        layout.addWidget(self.NoteLabel)
        layout.addWidget(self.Note)

        layout.addWidget(self.PrivateNoteLabel)
        layout.addWidget(self.PrivateNote) 


        # OK Button
        ok_button = QPushButton("OK")
        layout.addWidget(ok_button)

        # Set layout for the dialog
        self.dialog.setLayout(layout)
        ok_button.clicked.connect(self.ok_button_clicked)

        self.dialog.exec_()
        sql = SqlModelManager()
        # self.NewRecord = self.EnterAccoundData
        try: 
         sql.add_item(Table_widget,username_key=f"{self.ui.Username_LineEdit.text().strip()}" ,catagory=f"{self.mainwindow.treeWidget.selectedItems()[0].text(0)}" , tag_Label = f"{self.AccoundData[0]}"\
                    ,username = f"{self.AccoundData[1]}",password = f"{self.AccoundData[2]}", URL = f"{self.AccoundData[3]}",note = f"{self.AccoundData[4]}"\
                    ,privet_note = f"{self.AccoundData[5]}")
        except AttributeError:
            pass
        self.update_table()
       except IndexError:
                MessegeBox = QtWidgets.QMessageBox()
                MessegeBox.setText(F"You should select a Catgory first")
                MessegeBox.setWindowTitle("Erorr massage")
                MessegeBox.exec_()  

        # Button click event handler
    def ok_button_clicked(self):
            
            self.TagItem = self.Tag.text()
            self.UsernameItem = self.Username.text()
            self.PasswordItem = self.Password.text()
            self.URLItem = self.URL.text()
            self.NoteItem = self.Note.text()
            self.PrivateNoteItem = self.PrivateNote.text()

            self.AccoundData = [self.TagItem,self.UsernameItem,self.PasswordItem,self.URLItem,self.NoteItem,self.PrivateNoteItem]
            # print(f"the accound data list before encrypation : {self.AccoundData}")

            self.obj1 = Encryption()
            self.obj1.initialize_cipher(self.ui.Password_LineEdit.text())

            self.AccoundData[2] = self.obj1.encrypt(self.PasswordItem)

            self.AccoundData[5] = self.obj1.encrypt(self.PrivateNoteItem)

            # print(f"the accound data list after encryption : {self.AccoundData}")

            self.dialog.accept()
                
if __name__ == "__main__":
    object1 = SessionController()
    object1.init()

    


