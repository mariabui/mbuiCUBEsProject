from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton
from db_handler import get_user_from_db, save_user_to_db, open_db, close_db, save_claim_to_db


class ClaimWindow(QWidget):
    def __init__(self, db_entry):
        super().__init__()
        self.db_entry = db_entry
        self.email = None
        self.first_name = None
        self.last_name = None
        self.title = None
        self.department = None
        self.submit_email_button = None
        self.submit_user_button = None
        self.user_record = None
        self.setup()

    def setup(self):
        self.setWindowTitle(f'Claim Entry {self.db_entry[0]}')
        self.setGeometry(950, 0, 400, 300)
        email_label = QLabel('Email *', self)
        email_label.move(50, 30)
        self.email = QLineEdit(self)
        self.email.move(50, 45)
        self.submit_email_button = QPushButton('Submit', self)
        self.submit_email_button.clicked.connect(self.submit_email)
        self.submit_email_button.resize(self.submit_email_button.sizeHint())
        self.submit_email_button.move(170, 265)
        self.show()

    def generate_line(self, field: int, label_text: str, label_x: int, label_y: int, line_x: int, line_y: int, width=None):
        label = QLabel(label_text, self)
        label.move(label_x, label_y)
        line = QLineEdit('', self) if not self.user_record[0][field] else QLineEdit(self.user_record[0][field], self)
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

    def submit_email(self):
        print('clicked submit email')
        self.user_record = get_user_from_db('cubes_db.sqlite', self.email.text())
        print(self.user_record)
        self.check_user_exists_in_db(self.user_record)
        self.submit_email_button.hide()

    def check_user_exists_in_db(self, user_record: list):
        name_label = QLabel('Name *', self)
        name_label.move(50, 75)
        name_label.show()
        self.submit_user_button = QPushButton('Submit', self)
        self.submit_user_button.clicked.connect(self.submit_user_and_claim)
        self.submit_user_button.resize(self.submit_user_button.sizeHint())
        self.submit_user_button.move(170, 265)
        self.submit_user_button.show()
        if len(user_record) == 0:
            print('email in not db')
            self.first_name = self.generate_field('First', 50, 110, 50, 90)
            self.last_name = self.generate_field('Last', 175, 110, 175, 90)
            self.title = self.generate_field('Title *', 50, 135, 50, 150)
            self.department = self.generate_field('Department', 50, 180, 50, 195)
        else:
            print('email in db')
            self.first_name = self.generate_line(1, 'First', 50, 110, 50, 90)
            self.last_name = self.generate_line(2, 'Last', 175, 110, 175, 90)
            self.title = self.generate_line(3, 'Title *', 50, 135, 50, 150, 250)
            self.department = self.generate_line(4, 'Department *', 50, 180, 50, 195)
            self.save_claim()

    def submit_user_and_claim(self):
        print('clicked submit user data')
        connection, cursor = open_db('cubes_db.sqlite')
        save_user_to_db(tuple([self.email.text(), self.first_name.text(), self.last_name.text(), self.title.text(), self.department.text()]), cursor)
        print('saved user to db')
        close_db(connection, cursor)
        self.save_claim()
        print('saved claim to db')
        self.first_name.setReadOnly(True)
        self.last_name.setReadOnly(True)
        self.title.setReadOnly(True)
        self.department.setReadOnly(True)

    def save_claim(self):
        connection, cursor = open_db('cubes_db.sqlite')
        save_claim_to_db(tuple([self.db_entry[0], self.email.text()]), cursor)
        close_db(connection, cursor)
        self.email.setReadOnly(True)
        self.submit_user_button.setDisabled(True)