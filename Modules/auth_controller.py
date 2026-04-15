import sys, sqlite3, os ,sqlalchemy
from PyQt5 import QtCore, QtGui, QtWidgets , uic
from Modules.login import Ui_Login as loginmainClass
from Modules.Mainwindow import Ui_MainWindow as mainwindow 
import Modules.encryption
import Modules.sqlmodel_manager
from Modules.sqlmodel_manager import Catagory,Users,Table_widget,SqlModelManager 
from Modules.database_controller import DatabaseController
from os import path


class AuthController():
    # def __init__(self,ui) -> None:
    #     self.ui = ui
    def widjet(self):
        app = QtWidgets.QApplication(sys.argv)
        self.Login = QtWidgets.QMainWindow()
        self.ui =loginmainClass()
        self.ui.setupUi(self.Login)
        self.Login.show()

        self.mainwindo = QtWidgets.QMainWindow()
        self.mainwindow = mainwindow()
        self.mainwindow.setupUi(self.mainwindo)
        
        
        
    def starter(self):
        
        
        #all defs
        self.db = Modules.sqlmodel_manager.SqlModelManager()
      
        self.widjet()
        self.clicked()
        self.addCatagory()
        


        
        
        # sys.exit(app.exec_())  
        
    
      
          
    def clicked(self):
       
        self.ui.SignUp_btn.clicked.connect( self.signuppage)
        self.ui.Login_btn.clicked.connect(self.cheak)
        self.mainwindow.AddCatgory_btn.clicked.connect(self.addCatagory)
        self.mainwindow.lineEdit.textChanged.connect(self.searchbar)
        
        
    def signuppage(self):    
        self.ui.stackedWidget.setCurrentIndex(1) 

    def show_mainwindow(self):
        self.mainwindo.show()
        self.Login.close()       

    def cheak (self):   

        self.username = self.ui.Username_LineEdit.text().strip()
        self.password = self.ui.Password_LineEdit.text()
        self.accepted = False
        decrypet = Modules.encryption.Encryption()
       
        users = self.db.read(Users)

        for user in users:
                #user is taking from the list wich return to the main class Users that have the attrtuibe username and password 
                try:
                    decrypet.initialize_cipher(self.password)
                except Exception:
                    continue

                if self.username == user.username and self.password == decrypet.decrypt(user.password):
                    self.show_mainwindow()
                    DatabaseController.update_for_tree(self)
                    break
        else:
                     MessegeBox = QtWidgets.QMessageBox()
                     MessegeBox.setText("Username or password is inncorect")
                     MessegeBox.setWindowTitle("Erorr messege")
            
            
                     MessegeBox.exec_()        
                    
    
        
        

    def addCatagory (self):
        self.tree = self.mainwindow.treeWidget
        self.tree.columnCount()
        self.tree.setHeaderLabels(["General"])
        
        self.listss = QtWidgets.QInputDialog(self.mainwindo)
        self.listss.move(200,40)
        self.listss.setWindowTitle("Add New Catagory")
        self.listss.setLabelText("Enter the name of the new catagory")
        
        
        if self.listss.exec_() == QtWidgets.QInputDialog.Accepted :
            if  (self.listss.textValue() == "" or self.listss.textValue().isspace()):
                MessegeBox = QtWidgets.QMessageBox()
                MessegeBox.setText("You shoudn't be space")
                MessegeBox.setWindowTitle("Erorr messege")
                MessegeBox.exec_()  
            else:
                self.newcatlog = self.listss.textValue()
                try:
                    self.manager = SqlModelManager()
                    self.manager.add_item(Catagory, username_key=f"{self.username}" ,catagory=f"{self.newcatlog}")
                    self.accepted = True
                    
                except sqlalchemy.exc.IntegrityError:
                     MessegeBox = QtWidgets.QMessageBox()
                     MessegeBox.setText("This catagory is already exist")
                     MessegeBox.setWindowTitle("Erorr messege")
                     MessegeBox.exec_()
                if self.accepted : 
                        self.item = QtWidgets.QTreeWidgetItem(self.tree)
                        self.item.setText(0, f"{self.newcatlog}")
    
    def searchbar(self):
        self.search_text = self.mainwindow.lineEdit.text().lower()
        for row in range(self.mainwindow.tableWidget.rowCount()):
            self.row_matches = False
            
            for col in range(self.mainwindow.tableWidget.columnCount()):
                self.cell_content = self.mainwindow.tableWidget.item(row, col)
                if self.cell_content is not None and self.search_text in self.cell_content.text().lower():
                    self.row_matches = True
                    break
                
            self.mainwindow.tableWidget.setRowHidden(row, not self.row_matches)
           
    
if __name__ == "__main__":
    x = AuthController()
    x.starter()
    
  
    
    
    
    

        

            



        
        
        #connect
        
    
    
  
    
            
