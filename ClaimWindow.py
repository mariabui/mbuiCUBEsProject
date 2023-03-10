from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QListWidgetItem
from PySide6.QtGui import QColor
from db_handler import open_db, close_db, get_user_record_from_db, save_user_to_db, save_claim_to_db


class ClaimWindow(QWidget):
    def __init__(self, db_filename: str, entry_record: tuple, current: QListWidgetItem):
        super().__init__()
        self.db_filename = db_filename
        self.entry_record = entry_record
        self.selected_list_item = current
        self.bsu_email = None
        self.bsu_email_label = None
        self.first_name = None
        self.first_name_label = None
        self.last_name = None
        self.last_name_label = None
        self.title = None
        self.title_label = None
        self.department = None
        self.department_label = None
        self.submit_button = None
        self.claim_button = None
        self.user_record = None
        self.setup()

    def setup(self):
        self.setWindowTitle(f'Claim Entry {self.entry_record[0]}')
        self.setGeometry(950, 0, 400, 300)
        instructions = QLabel('Please fill out the information below:', self)
        instructions.move(95, 10)
        self.bsu_email, self.bsu_email_label = self.generate_field('Email *', 50, 30, 50, 45, 265)
        self.first_name, self.first_name_label = self.generate_field('First', 50, 110, 50, 90)
        self.last_name, self.last_name_label = self.generate_field('Last', 190, 110, 190, 90)
        self.title, self.title_label = self.generate_field('Title *', 50, 135, 50, 150, 265)
        self.department, self.department_label = self.generate_field('Department *', 50, 180, 50, 195, 265)
        self.submit_button = QPushButton('Submit', self)
        self.submit_button.clicked.connect(self.show_fields_and_claim_button)
        self.submit_button.resize(self.submit_button.sizeHint())
        self.submit_button.move(170, 265)
        self.show()

    def generate_field(self, label_text: str, label_x: int, label_y: int, field_x: int, field_y: int, width=None):
        label = QLabel(label_text, self)
        label.move(label_x, label_y)
        field = QLineEdit(self)
        field.move(field_x, field_y)
        if width:
            field.setFixedWidth(width)
        if label_text == 'Email *':
            label.show()
            field.show()
        else:
            label.hide()
            field.hide()
        return field, label

    def user_exists(self):
        self.user_record = get_user_record_from_db(self.db_filename, self.bsu_email.text())
        if len(self.user_record) == 0:
            return False
        else:
            return True

    def show_fields_and_claim_button(self):
        self.submit_button.hide()
        name_label = QLabel('Name *', self)
        name_label.move(50, 75)
        name_label.show()
        self.first_name.show()
        self.first_name_label.show()
        self.last_name.show()
        self.last_name_label.show()
        self.title.show()
        self.title_label.show()
        self.department.show()
        self.department_label.show()
        self.claim_button = QPushButton('Claim', self)
        self.claim_button.clicked.connect(self.claim)
        self.claim_button.resize(self.claim_button.sizeHint())
        self.claim_button.move(170, 265)
        self.claim_button.show()
        if self.user_exists():
            self.autofill_user_data()

    def autofill_user_data(self):
        self.bsu_email.setText(self.user_record[0][0])
        self.first_name.setText(self.user_record[0][1])
        self.last_name.setText(self.user_record[0][2])
        self.title.setText(self.user_record[0][3])
        self.department.setText(self.user_record[0][4])

    def save_user_and_claim_to_db(self):
        connection, cursor = open_db(self.db_filename)
        save_user_to_db(tuple([self.bsu_email.text(), self.first_name.text(), self.last_name.text(),
                               self.title.text(), self.department.text()]), cursor)
        save_claim_to_db(tuple([self.entry_record[0], self.bsu_email.text()]), cursor)
        close_db(connection, cursor)

    def claim(self):
        self.save_user_and_claim_to_db()
        self.bsu_email.setReadOnly(True)
        self.first_name.setReadOnly(True)
        self.last_name.setReadOnly(True)
        self.title.setReadOnly(True)
        self.department.setReadOnly(True)
        self.claim_button.setDisabled(True)
        self.selected_list_item.setForeground(QColor('darkRed'))
        success_message = QLabel('Successfully claimed!', self)
        success_message.move(135, 235)
        success_message.show()
