from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QComboBox, QCheckBox


class EntryDataWindow(QWidget):
    def __init__(self, entry: dict):
        super().__init__()
        self.entry = entry
        self.setup()

    def setup(self):
        self.setWindowTitle(f"Entry {self.entry['EntryId']}")
        self.setGeometry(450, 0, 500, 900)

        self.generate_drop_box('Field1', 'Prefix', ['', 'Mr.', 'Ms.', 'Dr.'], 50, 50, 40, 65)

        name_label = QLabel(self)
        name_label.setText('Name *')
        name_label.move(50, 90)
        self.generate_line('Field2', 'First', 50, 130, 50, 110)
        self.generate_line('Field3', 'Last', 190, 130, 190, 110)
        self.generate_line('Field4', 'Title *', 50, 150, 50, 170, 200)
        self.generate_line('Field5', 'Organization Name *', 50, 190, 50, 210, 200)
        self.generate_line('Field6', 'Email *', 50, 230, 50, 250, 200)
        self.generate_line('Field7', 'Organization Website', 50, 270, 50, 290, 200)
        self.generate_line('Field8', 'Phone Number', 50, 310, 50, 330)

        collab_label = QLabel(self)
        collab_label.setText('Which of the following collaborative opportunities\n'
                             'would you be interested in? (check all that apply)')
        collab_label.move(50, 350)
        self.generate_checkbox('Field9', 'Course Project', 50, 390, 75, 390)
        self.generate_checkbox('Field10', 'Guest Speaker', 50, 410, 75, 410)
        self.generate_checkbox('Field11', 'Site Vist', 50, 430, 75, 430)
        self.generate_checkbox('Field12', 'Job Shadow', 50, 450, 75, 450)
        self.generate_checkbox('Field13', 'Internships', 50, 470, 75, 470)
        self.generate_checkbox('Field14', 'Career Panel', 50, 490, 75, 490)
        self.generate_checkbox('Field15', 'Networking Event', 50, 510, 75, 510)

        collab_time_label = QLabel(self)
        collab_time_label.setText('Your proposed collaboration time period')
        collab_time_label.move(50, 530)
        self.generate_checkbox('Field109', 'Summer 2022 (June 2022- August 2022)', 50, 550, 75, 550)
        self.generate_checkbox('Field110', 'Fall 2022 (September 2022- December 2022)', 50, 570, 75, 570)
        self.generate_checkbox('Field111', 'Spring 2023 (January 2023- April 2023)', 50, 590, 75, 590)
        self.generate_checkbox('Field112', 'Summer 2023 (June 2023- August 2023)', 50, 610, 75, 610)
        self.generate_checkbox('Field113', 'Other', 50, 630, 75, 630)

        self.generate_drop_box('Field210', 'If you participate in a CUBEs project, do we have your\n'
                                           'permission to use your organizations name upon\n'
                                           'completion, when listing completed projects?',
                               ['Yes', 'No', 'Further discussion is needed'], 50, 650, 40, 700)

    def generate_drop_box(self, field: str, label: str, items: list, label_x: int,
                          label_y: int, drop_down_x: int, drop_down_y: int):
        q_label = QLabel(self)
        q_label.setText(label)
        q_label.move(label_x, label_y)
        drop_down = QComboBox(self)
        drop_down.addItems(items)
        drop_down.setCurrentText(self.entry[field])
        drop_down.move(drop_down_x, drop_down_y)
        drop_down.setDisabled(True)

    def generate_line(self, field: str, label: str, label_x: int, label_y: int, line_x: int, line_y: int, width=None):
        q_label = QLabel(self)
        q_label.setText(label)
        q_label.move(label_x, label_y)
        line = QLineEdit(self.entry[field], self)
        line.move(line_x, line_y)
        if width:
            line.setFixedWidth(width)
        line.setReadOnly(True)

    def checked_or_unchecked(self, checkbox: QCheckBox, field: str):
        if self.entry[field] == '':
            checkbox.setChecked(False)
        else:
            checkbox.setChecked(True)

    def generate_checkbox(self, field: str, label: str, checkbox_x: int, checkbox_y: int, label_x: int, label_y: int, ):
        q_label = QLabel(self)
        q_label.setText(label)
        q_label.move(label_x, label_y)
        checkbox = QCheckBox(self)
        self.checked_or_unchecked(checkbox, field)
        checkbox.move(checkbox_x, checkbox_y)
        checkbox.setEnabled(False)
