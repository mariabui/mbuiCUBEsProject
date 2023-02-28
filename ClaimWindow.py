from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QListWidgetItem
from PySide6.QtGui import QColor
from db_handler import get_user_record, save_user_to_users_table, open_db, close_db, save_claim_to_claims_table


class ClaimWindow(QWidget):
    def __init__(self, db_entry: tuple, current: QListWidgetItem, db_filename: str):
        super().__init__()
        self.db_entry = db_entry
        self.db_filename = db_filename
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
        email_label = QLabel('Email *', self)
        email_label.move(50, 30)
        self.email = QLineEdit(self)
        self.email.move(50, 45)
        self.submit_email_button = QPushButton('Submit', self)
        self.submit_email_button.clicked.connect(self.show_lines_or_fields)
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

    def user_exists(self):
        self.user_record = get_user_record(self.db_filename, self.email.text())
        print(f'user record: {self.user_record}')
        self.submit_email_button.hide()
        if len(self.user_record) == 0:
            print('user does not exist')
            return False
        else:
            print('user exists')
            return True

    def show_lines_or_fields(self):
        print('clicked submit email')
        name_label = QLabel('Name *', self)
        name_label.move(50, 75)
        name_label.show()
        self.claim_button = QPushButton('Claim', self)
        self.claim_button.clicked.connect(self.claim)
        self.claim_button.resize(self.claim_button.sizeHint())
        self.claim_button.move(170, 265)
        self.claim_button.show()
        if self.user_exists():
            self.email.setReadOnly(True)
            self.first_name = self.generate_line(1, 'First', 50, 110, 50, 90)
            self.last_name = self.generate_line(2, 'Last', 175, 110, 175, 90)
            self.title = self.generate_line(3, 'Title *', 50, 135, 50, 150, 250)
            self.department = self.generate_line(4, 'Department *', 50, 180, 50, 195)
        else:
            self.first_name = self.generate_field('First', 50, 110, 50, 90)
            self.last_name = self.generate_field('Last', 175, 110, 175, 90)
            self.title = self.generate_field('Title *', 50, 135, 50, 150)
            self.department = self.generate_field('Department', 50, 180, 50, 195)

    def save_user_to_users_table(self):
        connection, cursor = open_db(self.db_filename)
        save_user_to_users_table(tuple([self.email.text(), self.first_name.text(), self.last_name.text(),
                                        self.title.text(), self.department.text()]), cursor)
        close_db(connection, cursor)

    def save_claim_to_claims_table(self):
        connection, cursor = open_db(self.db_filename)
        save_claim_to_claims_table(tuple([self.db_entry[0], self.email.text()]), cursor)
        close_db(connection, cursor)

    def claim(self):
        if self.user_exists():
            self.save_claim_to_claims_table()
        else:
            self.save_user_to_users_table()
            self.save_claim_to_claims_table()
            self.first_name.setReadOnly(True)
            self.last_name.setReadOnly(True)
            self.title.setReadOnly(True)
            self.department.setReadOnly(True)
        self.email.setReadOnly(True)
        self.current.setForeground(QColor('red'))
        self.claim_button.setDisabled(True)
        print('clicked claim button')
