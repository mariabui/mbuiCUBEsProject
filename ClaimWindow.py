from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton
from db_handler import get_email_from_db, save_user_to_db, open_db, close_db, save_claim_to_db


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
        self.user_record = None
        self.setup()

    def setup(self):
        self.setWindowTitle(f'Claim Entry {self.db_entry[0]}')
        self.setGeometry(950, 0, 450, 470)
        self.email = self.generate_email_field()
        self.submit_email_button = QPushButton('Submit', self)
        self.submit_email_button.clicked.connect(self.submit_email)
        self.submit_email_button.resize(self.submit_email_button.sizeHint())
        self.submit_email_button.move(200, 430)
        self.show()


    def generate_email_field(self):
        label = QLabel('Email', self)
        label.move(50, 30)
        line = QLineEdit(self)
        line.move(50, 45)
        return line

    def generate_line(self, field: int, label_text: str, label_x: int, label_y: int, line_x: int, line_y: int, width=None):
        label = QLabel(label_text, self)
        label.move(label_x, label_y)
        line = QLineEdit('', self) if not self.user_record[field] else QLineEdit(self.user_record[field], self)
        line.move(line_x, line_y)
        if width:
            line.setFixedWidth(width)
        line.setReadOnly(True)
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
        email_text = self.email.text()
        self.user_record = get_email_from_db('cubes_db.sqlite', email_text)
        print(self.user_record)
        self.check_email_exists_in_db(self.user_record)
        self.submit_email_button.hide()

    def submit_user_data(self):
        print('clicked submit user data')
        connection, cursor = open_db('cubes_db.sqlite')
        save_user_to_db(tuple([self.email.text(), self.first_name.text(), self.last_name.text(), self.title.text(),
                               self.department.text()]), cursor)
        print('saved user to db')
        save_claim_to_db(tuple([self.db_entry[0], self.email.text()]), cursor)
        print('saved claim to db')
        close_db(connection, cursor)


    def check_email_exists_in_db(self, user_record: list):
        name_label = QLabel('Name *', self)
        name_label.move(50, 75)
        name_label.show()
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
            self.department = self.generate_line(4, 'Department', 50, 180, 50, 195)
        submit_button = QPushButton('Submit', self)
        submit_button.clicked.connect(self.submit_user_data)
        submit_button.resize(submit_button.sizeHint())
        submit_button.move(200, 430)
        submit_button.show()