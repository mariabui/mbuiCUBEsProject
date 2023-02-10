from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QComboBox, QCheckBox


class EntryDataWindow(QWidget):
    def __init__(self, entry: dict):
        super().__init__()
        self.entry = entry
        self.setup()

    def setup(self):
        self.setWindowTitle(f"Entry {self.entry['EntryId']}")
        self.setGeometry(450, 0, 500, 900)
        prefix_label = QLabel(self)
        prefix_label.setText('Prefix')
        prefix_label.move(50, 50)
        prefix_drop_down = QComboBox(self)
        prefix_drop_down.addItems(['', 'Mr.', 'Ms.', 'Dr.'])
        prefix_drop_down.setCurrentText(self.entry['Field1'])
        prefix_drop_down.move(40, 65)
        prefix_drop_down.setDisabled(True)

        name_label = QLabel(self)
        name_label.setText('Name *')
        name_label.move(50, 90)
        first_name = QLineEdit(self.entry['Field2'], self)
        first_name.move(50, 110)
        first_name_label = QLabel(self)
        first_name_label.setText('First')
        first_name_label.move(50, 130)
        last_name = QLineEdit(self.entry['Field3'], self)
        last_name.move(190, 110)
        last_name_label = QLabel(self)
        last_name_label.setText('Last')
        last_name_label.move(190, 130)

        title_label = QLabel(self)
        title_label.setText('Title *')
        title_label.move(50, 150)
        title = QLineEdit(self.entry['Field4'], self)
        title.move(50, 170)

        org_name_label = QLabel(self)
        org_name_label.setText('Organization Name *')
        org_name_label.move(50, 190)
        org_name = QLineEdit(self.entry['Field5'], self)
        org_name.move(50, 210)
        org_name.setFixedWidth(200)
        org_name.setReadOnly(True)

        email_label = QLabel(self)
        email_label.setText('Email *')
        email_label.move(50, 230)
        email = QLineEdit(self.entry['Field6'], self)
        email.move(50, 250)

        org_web_label = QLabel(self)
        org_web_label.setText('Organization Website')
        org_web_label.move(50, 270)
        org_web = QLineEdit(self.entry['Field7'], self)
        org_web.move(50, 290)

        phone_num_label = QLabel(self)
        phone_num_label.setText('Phone Number')
        phone_num_label.move(50, 310)
        phone_num = QLineEdit(self.entry['Field8'], self)
        phone_num.move(50, 330)

        collab_label = QLabel(self)
        collab_label.setText('Which of the following collaborative opportunities\n'
                             'would you be interested in? (check all that apply)')
        collab_label.move(50, 350)
        course_project_label = QLabel(self)
        course_project_label.setText('Course Project')
        course_project_label.move(75, 390)
        course_project_checkbox = QCheckBox(self)
        self.checked_or_unchecked(course_project_checkbox, 'Field9')
        course_project_checkbox.move(50, 390)
        course_project_checkbox.setEnabled(False)

        guest_speaker_label = QLabel(self)
        guest_speaker_label.setText('Guest Speaker')
        guest_speaker_label.move(75, 410)
        guest_speaker_checkbox = QCheckBox(self)
        self.checked_or_unchecked(guest_speaker_checkbox, 'Field10')
        guest_speaker_checkbox.move(50, 410)

    def checked_or_unchecked(self, checkbox: QCheckBox, field: str):
        if self.entry[field] == '':
            checkbox.setChecked(False)
        else:
            checkbox.setChecked(True)
