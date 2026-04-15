from Modules.login import Ui_Login
from Modules.Mainwindow import Ui_MainWindow
from Modules.sqlmodel_manager import SqlModelManager  , Table_widget 
from Modules.encryption import Encryption
import sys
from PyQt5 import  QtWidgets
import  cryptography.fernet 
#omars class
class OmarClass():
    def init(self):
        
         self.app = QtWidgets.QApplication(sys.argv)
         self.Login = QtWidgets.QMainWindow()
         self.ui = Ui_Login()
         self.ui.setupUi(self.Login)

         self.mainwindo = QtWidgets.QMainWindow()
         self.mainwindow = Ui_MainWindow()
         self.mainwindow.setupUi(self.mainwindo)
         self.omar()

    def omar(self):
        self.ui.return_to_login.mousePressEvent =self.return_to_Loginbtn
        self.mainwindow.treeWidget.itemSelectionChanged.connect(self.update_table)
        self.ui.pushButton.clicked.connect(self.showpassword_login)
        self.ui.pushButton_2.clicked.connect(self.showpassword_sginup)
    def showpassword_sginup(self):
         if self.ui.Password_LineEdit_p2.echoMode() == QtWidgets.QLineEdit.EchoMode.Password:
            self.ui.Password_LineEdit_p2.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
         else:
            self.ui.Password_LineEdit_p2.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
    def showpassword_login(self):
        if self.ui.Password_LineEdit.echoMode() == QtWidgets.QLineEdit.EchoMode.Password:
            self.ui.Password_LineEdit.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
        else:
             self.ui.Password_LineEdit.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
    
    def return_to_Loginbtn(self , event):# if the label preesed return to the login page 
       
        if event:
            self.ui.Username_LineEdit_p2.clear()#clear the line edits
            self.ui.Password_LineEdit_p2.clear()
            self.ui.Username_LineEdit.clear()
            self.ui.Password_LineEdit.clear()
            self.ui.stackedWidget.setCurrentIndex(0)
    """
    get the items from the data base then put it in the main window if a catagory ciliked
    """
    def update_table(self):
        sql = SqlModelManager()
        data = sql.read(Table_widget)
        try: #store "item" in list (the item store only items that have the same username and same catagory) 
            reqierdData =  [item for item in data if item.username_key == self.ui.Username_LineEdit.text().strip() and item.catagory == self.mainwindow.treeWidget.selectedItems()[0].text(0)]
        
        
            self.mainwindow.tableWidget.clearContents()#delete all items
            self.mainwindow.tableWidget.setRowCount(0)#delete all rows
        
            if reqierdData==[]:#if requried data is empty put none in table
                self.mainwindow.tableWidget.setItem(0, 4, QtWidgets.QTableWidgetItem())
            else:
                for row, table_item in enumerate(reqierdData):# itreate each item while keeping the index in row 
                    #just display these items to table (names taked from the sqlmodelmanger)
                    columns_to_display = ["tag_Label", "username", "password", "URL"]
                    self.mainwindow.tableWidget.insertRow(row)#insert row for each item 
                    for col, column_name in enumerate(columns_to_display):
                        #if the item reached password decrypteded and masked it 
                        if column_name == "password":
                        #the try except beacuse if there is no password it will cause error so add the items as none
                         try:
                            encrypet = Encryption()
                            decrypted_password = encrypet.decrypt(getattr(table_item, column_name))  # decreypt the password
                            masked_password = "•"*len(decrypted_password)  # mask it
                            
                            self.mainwindow.tableWidget.setItem(row, col, QtWidgets.QTableWidgetItem(masked_password))
                         except cryptography.fernet.InvalidToken :#no password or item is empty
                            self.mainwindow.tableWidget.setItem(row, col, QtWidgets.QTableWidgetItem(getattr(table_item, column_name)))
                                
                        else:
                            self.mainwindow.tableWidget.setItem(row, col, QtWidgets.QTableWidgetItem(getattr(table_item, column_name)))#add the item (taked from the column name) to the tablewidget
        except IndexError: #if he want to not select a catagory
            pass
