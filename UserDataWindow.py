from PySide6.QtWidgets import QWidget, QLabel, QLineEdit
from db_handler import get_claim_record_from_db, get_user_record_from_db


class UserDataWindow(QWidget):
    def __init__(self, db_filename: str, entry_record: tuple):
        super().__init__()
        self.db_filename = db_filename
        self.entry_record = entry_record
        self.bsu_email = None
        self.first_name = None
        self.last_name = None
        self.title = None
        self.department = None
        self.claim_record = None
        self.user_record = None
        self.setup()

    def setup(self):
        self.setWindowTitle(f'Entry {self.entry_record[0]} Claimed By')
        self.setGeometry(950, 0, 400, 260)
        self.bsu_email = self.generate_field(0, 'Email *', 50, 30, 50, 45, 265)
        name_label = QLabel('Name *', self)
        name_label.move(50, 75)
        self.first_name = self.generate_field(1, 'First', 50, 110, 50, 90)
        self.last_name = self.generate_field(2, 'Last', 190, 110, 190, 90)
        self.title = self.generate_field(3, 'Title *', 50, 135, 50, 150, 265)
        self.department = self.generate_field(4, 'Department *', 50, 180, 50, 195, 265)
        self.show()

    def entry_is_claimed(self, entry_record: tuple):
        self.claim_record = get_claim_record_from_db(self.db_filename, entry_record[0])
        if len(self.claim_record) == 0:
            return False
        else:
            return True

    def generate_field(self, field: int, label_text: str, label_x: int, label_y: int, field_x: int, field_y: int, width=None):
        if self.entry_is_claimed(self.entry_record):
            self.user_record = get_user_record_from_db(self.db_filename, self.claim_record[0][2])
            label = QLabel(label_text, self)
            label.move(label_x, label_y)
            line = QLineEdit(self.user_record[0][field], self)
            line.move(field_x, field_y)
            if width:
                line.setFixedWidth(width)
            line.setReadOnly(True)
            return line
