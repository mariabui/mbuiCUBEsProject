from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton
from db_handler import get_user_from_db, save_user_to_db, open_db, close_db, save_claim_to_db, get_entry_claim_from_db


class UserDataWindow(QWidget):
    def __init__(self, db_entry: tuple):
        super().__init__()
        self.db_entry = db_entry
        self.user_record = None
        self.email = None
        self.first_name = None
        self.last_name = None
        self.title = None
        self.department = None
        self.setup()

    def setup(self):
        self.setWindowTitle(f'User')
        self.setGeometry(950, 0, 400, 300)
        self.email = self.generate_line(0, 'Email', 50, 30, 50, 45, 265)
        name_label = QLabel('Name *', self)
        name_label.move(50, 75)
        self.first_name = self.generate_line(1, 'First', 50, 110, 50, 90)
        self.last_name = self.generate_line(2, 'Last', 190, 110, 190, 90)
        self.title = self.generate_line(3, 'Title *', 50, 135, 50, 150, 265)
        self.department = self.generate_line(4, 'Department', 50, 180, 50, 195, 265)
        self.show()

    def generate_line(self, field: int, label_text: str, label_x: int, label_y: int, line_x: int, line_y: int, width=None):
        entry_claim_record = get_entry_claim_from_db('cubes_db.sqlite', self.db_entry)
        print(entry_claim_record)
        if len(entry_claim_record) != 0:
            self.user_record = get_user_from_db('cubes_db.sqlite', entry_claim_record[0][1])
            print(self.user_record)
            label = QLabel(label_text, self)
            label.move(label_x, label_y)
            line = QLineEdit('', self) if not self.user_record[0][field] else QLineEdit(self.user_record[0][field], self)
            line.move(line_x, line_y)
            if width:
                line.setFixedWidth(width)
            line.setReadOnly(True)
            return line
