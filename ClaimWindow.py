from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QListWidgetItem
from PySide6.QtGui import QColor
from db_handler import open_db, close_db, get_user_record_from_db, save_user_to_db, save_claim_to_db


class ClaimWindow(QWidget):
    def __init__(self, db_filename: str, db_entry: tuple, current: QListWidgetItem):
        super().__init__()
        self.db_filename = db_filename
        self.db_entry = db_entry
        self.current = current
        self.email = None
        self.first_name = None
        self.last_name = None
        self.title = None
        self.department = None
        self.submit_email_button = None
        self.claim_button = None
        self.user_record = None
        self.setup()

    def setup(self):
        self.setWindowTitle(f'Claim Entry {self.db_entry[0]}')
        self.setGeometry(950, 0, 400, 300)
        instructions = QLabel('Please fill out the information below. ', self)
        instructions.move(95, 10)
        self.email = self.generate_field('Email *', 50, 30, 50, 45)
        self.submit_email_button = QPushButton('Submit', self)
        self.submit_email_button.clicked.connect(self.show_lines_or_fields)
        self.submit_email_button.resize(self.submit_email_button.sizeHint())
        self.submit_email_button.move(170, 265)
        self.show()

    def generate_line(self, field: int, label_text: str, label_x: int, label_y: int, line_x: int, line_y: int, width=None):
        label = QLabel(label_text, self)
        label.move(label_x, label_y)
        line = QLineEdit(self.user_record[0][field], self)
        line.move(line_x, line_y)
        if width:
            line.setFixedWidth(width)
        line.setReadOnly(True)
        label.show()
        line.show()
        return line

    def generate_field(self, label_text: str, label_x: int, label_y: int, field_x: int, field_y: int, width=None):
        label = QLabel(label_text, self)
        label.move(label_x, label_y)
        field = QLineEdit(self)
        field.move(field_x, field_y)
        if width:
            field.setFixedWidth(width)
        label.show()
        field.show()
        return field

    def user_exists(self):
        self.user_record = get_user_record_from_db(self.db_filename, self.email.text())
        print(f'user record: {self.user_record}')
        if len(self.user_record) == 0:
            return False
        else:
            return True

    def show_lines_or_fields(self):
        print('user clicked submit email')
        self.submit_email_button.hide()
        name_label = QLabel('Name *', self)
        name_label.move(50, 75)
        name_label.show()
        self.claim_button = QPushButton('Claim', self)
        self.claim_button.clicked.connect(self.claim)
        self.claim_button.resize(self.claim_button.sizeHint())
        self.claim_button.move(170, 265)
        self.claim_button.show()
        if self.user_exists():
            print('user exists, autofill user data')
            self.email.setReadOnly(True)
            self.first_name = self.generate_line(1, 'First', 50, 110, 50, 90)
            self.last_name = self.generate_line(2, 'Last', 175, 110, 175, 90)
            self.title = self.generate_line(3, 'Title *', 50, 135, 50, 150, 250)
            self.department = self.generate_line(4, 'Department *', 50, 180, 50, 195)
        else:
            print('user does not exist')
            self.first_name = self.generate_field('First', 50, 110, 50, 90)
            self.last_name = self.generate_field('Last', 175, 110, 175, 90)
            self.title = self.generate_field('Title *', 50, 135, 50, 150)
            self.department = self.generate_field('Department', 50, 180, 50, 195)

    def save_user_to_db(self):
        connection, cursor = open_db(self.db_filename)
        save_user_to_db(tuple([self.email.text(), self.first_name.text(), self.last_name.text(),
                               self.title.text(), self.department.text()]), cursor)
        close_db(connection, cursor)

    def save_claim_to_db(self):
        connection, cursor = open_db(self.db_filename)
        save_claim_to_db(tuple([self.db_entry[0], self.email.text()]), cursor)
        close_db(connection, cursor)

    def claim(self):
        print('user clicked claim button')
        if self.user_exists():
            self.save_claim_to_db()
            print('saved claim to db')
        else:
            self.save_user_to_db()
            print('saved user to db')
            self.save_claim_to_db()
            print('saved claim to db')
            self.email.setReadOnly(True)
            self.first_name.setReadOnly(True)
            self.last_name.setReadOnly(True)
            self.title.setReadOnly(True)
            self.department.setReadOnly(True)
        self.claim_button.setDisabled(True)
        self.current.setForeground(QColor('red'))
        success_message = QLabel('Successfully claimed!', self)
        success_message.move(135, 235)
        success_message.show()
