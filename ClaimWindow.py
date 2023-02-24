from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton


class ClaimWindow(QWidget):
    def __init__(self, db_entry):
        super().__init__()
        self.db_entry = db_entry
        self.email = None
        self.first_name = None
        self.last_name = None
        self.title = None
        self.department = None
        self.setup()

    def setup(self):
        self.setWindowTitle(f'Claim Entry {self.db_entry[0]}')
        self.setGeometry(950, 0, 450, 470)
        self.email = self.generate_email_field()
        submit_button = QPushButton('Submit', self)
        submit_button.clicked.connect(self.submit)
        submit_button.resize(submit_button.sizeHint())
        submit_button.move(200, 430)
        self.show()


    def generate_email_field(self):
        label = QLabel('Email', self)
        label.move(50, 30)
        line = QLineEdit(self)
        line.move(50, 45)
        return line

    def submit(self):
        print('clicked submit')