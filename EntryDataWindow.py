from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QComboBox, QCheckBox


class EntryDataWindow(QWidget):
    def __init__(self, db_entry: dict):
        super().__init__()
        self.db_entry = db_entry
        self.setup()

    def setup(self):
        self.setWindowTitle(f'Entry {self.db_entry[0]}')
        self.setGeometry(500, 0, 500, 900)

        self.generate_drop_down(1, 'Prefix', ['', 'Mr.', 'Ms.', 'Dr.'], 50, 10, 40, 25)

        name_label = QLabel('Name *', self)
        name_label.move(50, 60)
        self.generate_field(2, 'First', 50, 95, 50, 75)
        self.generate_field(3, 'Last', 180, 95, 180, 75)
        self.generate_field(4, 'Title *', 50, 120, 50, 135, 300)
        self.generate_field(5, 'Organization Name *', 50, 165, 50, 180, 300)
        self.generate_field(6, 'Email *', 50, 210, 50, 225, 300)
        self.generate_field(7, 'Organization Website', 50, 255, 50, 270, 300)
        self.generate_field(8, 'Phone Number', 50, 300, 50, 315)

        collab_label = QLabel('Which of the following collaborative opportunities would\n'
                              'you be interested in? (check all that apply)', self)
        collab_label.move(50, 345)
        self.generate_checkbox(9, 'Course Project', 50, 380, 75, 380)
        self.generate_checkbox(10, 'Guest Speaker', 50, 400, 75, 400)
        self.generate_checkbox(11, 'Site Vist', 50, 420, 75, 420)
        self.generate_checkbox(12, 'Job Shadow', 50, 440, 75, 440)
        self.generate_checkbox(13, 'Internships', 50, 460, 75, 460)
        self.generate_checkbox(14, 'Career Panel', 50, 480, 75, 480)
        self.generate_checkbox(15, 'Networking Event', 50, 500, 75, 500)

        collab_time_label = QLabel('Your proposed collaboration time period', self)
        collab_time_label.move(50, 530)
        self.generate_checkbox(16, 'Summer 2022 (June 2022- August 2022)', 50, 550, 75, 550)
        self.generate_checkbox(17, 'Fall 2022 (September 2022- December 2022)', 50, 570, 75, 570)
        self.generate_checkbox(18, 'Spring 2023 (January 2023- April 2023)', 50, 590, 75, 590)
        self.generate_checkbox(19, 'Summer 2023 (June 2023- August 2023)', 50, 610, 75, 610)
        self.generate_checkbox(20, 'Other', 50, 630, 75, 630)

        self.generate_drop_down(21, 'If you participate in a CUBEs project, do we have your\n'
                                    'permission to use your organizations name upon\n'
                                    'completion, when listing completed projects?',
                                ['Yes', 'No', 'Further discussion is needed'], 50, 660, 40, 710)

        self.show()

    def generate_drop_down(self, field: int, label_text: str, items: list, label_x: int,
                           label_y: int, drop_down_x: int, drop_down_y: int):
        label = QLabel(label_text, self)
        label.move(label_x, label_y)
        drop_down = QComboBox(self)
        drop_down.addItems(items)
        drop_down.setCurrentText(self.db_entry[field])
        drop_down.move(drop_down_x, drop_down_y)
        drop_down.setDisabled(True)

    def generate_field(self, field: int, label_text: str, label_x: int, label_y: int, line_x: int, line_y: int, width=None):
        label = QLabel(label_text, self)
        label.move(label_x, label_y)
        if not self.db_entry[field]:
            line = QLineEdit('', self)
        else:
            line = QLineEdit(self.db_entry[field], self)
        line.move(line_x, line_y)
        if width:
            line.setFixedWidth(width)
        line.setReadOnly(True)

    def checked_or_unchecked(self, checkbox: QCheckBox, field: int):
        if self.db_entry[field] == 'Y':
            checkbox.setChecked(True)
        else:
            checkbox.setChecked(False)

    def generate_checkbox(self, field: int, label_text: str, checkbox_x: int, checkbox_y: int, label_x: int, label_y: int, ):
        # label = QLabel(label_text, self)
        # label.setText(label_text)
        # label.move(label_x, label_y)
        checkbox = QCheckBox(label_text, self)
        self.checked_or_unchecked(checkbox, field)
        checkbox.move(checkbox_x, checkbox_y)
        checkbox.setDisabled(True)
