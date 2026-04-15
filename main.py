""""
Group B  project 

members:( name , id )
Omar Khalid Haddad ,  2236620
Marwan Ali , 2037061
Ibrahim Mohammed , 2135229
Hussam Al-Shikh 2036674
Bilal hassan 2136347
"""
from PyQt5 import QtCore, QtGui, QtWidgets
from Modules import login , Mainwindow
import Modules , sys
from Modules import encryption as omar
from Modules import Bilal as bilal
from Modules import Ibrahim as ibrahim
from Modules import Marwan as marwan
from Modules import Hussam as hussam
import Modules.sqlmodel_manager
from Modules.Omar import OmarClass

class Main(ibrahim.IbrahimClass , marwan.MarwanClass , hussam.HussamClass , omar.Encryption , OmarClass):
    def __init__(self):
        super().__init__()
        self.app = QtWidgets.QApplication(sys.argv)
        self.Login = QtWidgets.QMainWindow()
        self.ui = login.Ui_Login()
        self.ui.setupUi(self.Login)
        self.mainwindo = QtWidgets.QMainWindow()
        self.mainwindow = Mainwindow.Ui_MainWindow()
        self.mainwindow.setupUi(self.mainwindo)
        #connection
        self.db = Modules.sqlmodel_manager.SqlModelManager()
        # functions
        self.omar()
        self.clicked()
        self.marwan()
        self.click_btn()
      
        self.Login.show()

        sys.exit(self.app.exec_())

if __name__=="__main__":
    object1 = Main()