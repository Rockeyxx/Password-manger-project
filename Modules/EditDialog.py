from PyQt5 import QtWidgets, QtGui

class EditDialog2(QtWidgets.QDialog):
    def __init__(self, tag, username, password, url, note, private_note, parent=None):
        super(EditDialog2, self).__init__(parent)
        self.setWindowTitle("Edit Account")
        self.setGeometry(100, 100, 400, 250)

        self.tag_label = QtWidgets.QLabel("Tag/Label:")
        self.tag_line_edit = QtWidgets.QLineEdit(self)
        self.tag_line_edit.setText(tag)

        self.username_label = QtWidgets.QLabel("Username:")
        self.username_line_edit = QtWidgets.QLineEdit(self)
        self.username_line_edit.setText(username)

        self.password_label = QtWidgets.QLabel("Password:")
        self.password_line_edit = QtWidgets.QLineEdit(self)
        self.password_line_edit.setText(password)

        self.url_label = QtWidgets.QLabel("URL:")
        self.url_line_edit = QtWidgets.QLineEdit(self)
        self.url_line_edit.setText(url)

        self.note_label = QtWidgets.QLabel("Note:")
        self.note_line_edit = QtWidgets.QLineEdit(self)
        self.note_line_edit.setText(note)

        self.private_note_label = QtWidgets.QLabel("Private Note:")
        self.private_note_line_edit = QtWidgets.QLineEdit(self)
        self.private_note_line_edit.setText(private_note)

        self.save_button = QtWidgets.QPushButton("Save", self)
        self.save_button.clicked.connect(self.accept)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.tag_label)
        self.layout.addWidget(self.tag_line_edit)
        self.layout.addWidget(self.username_label)
        self.layout.addWidget(self.username_line_edit)
        self.layout.addWidget(self.password_label)
        self.layout.addWidget(self.password_line_edit)
        self.layout.addWidget(self.url_label)
        self.layout.addWidget(self.url_line_edit)
        self.layout.addWidget(self.note_label)
        self.layout.addWidget(self.note_line_edit)
        self.layout.addWidget(self.private_note_label)
        self.layout.addWidget(self.private_note_line_edit)
        self.layout.addWidget(self.save_button)

    def getData(self):
        tag = self.tag_line_edit.text()
        username = self.username_line_edit.text()
        password = self.password_line_edit.text()
        url = self.url_line_edit.text()
        note = self.note_line_edit.text()
        private_note = self.private_note_line_edit.text()

        return {'tag': tag, 'username': username, 'password': password, 'url': url, 'note': note, 'private_note': private_note}

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    edit_dialog = EditDialog2("Tag1", "User1", "Pass1", "http://example.com", "Note1", "PrivateNote1")
    result = edit_dialog.exec_()

    if result == QtWidgets.QDialog.Accepted:
        edited_data = edit_dialog.getData()
        print(edited_data)

       
