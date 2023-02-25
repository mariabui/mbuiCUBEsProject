from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QCheckBox


class EntryDataWindow(QWidget):
    def __init__(self, db_entry: tuple):
        super().__init__()
        self.db_entry = db_entry
        self.prefix = None
        self.first_name = None
        self.last_name = None
        self.title = None
        self.organization_name = None
        self.email = None
        self.organization_website = None
        self.phone_number = None
        self.course_project = None
        self.guest_speaker = None
        self.site_visit = None
        self.job_shadow = None
        self.internships = None
        self.career_panel = None
        self.networking_event = None
        self.summer_2022 = None
        self.fall_2022 = None
        self.spring_2023 = None
        self.summer_2023 = None
        self.other_time_period = None
        self.organization_name_usage = None
        self.setup()

    def setup(self):
        self.setWindowTitle(f'Entry {self.db_entry[0]}')
        self.setGeometry(500, 0, 450, 800)

        self.prefix = self.generate_line(1, 'Prefix', 50, 30, 50, 45)

        name_label = QLabel('Name *', self)
        name_label.move(50, 75)
        self.first_name = self.generate_line(2, 'First', 50, 110, 50, 90)
        self.last_name = self.generate_line(3, 'Last', 190, 110, 190, 90)
        self.title = self.generate_line(4, 'Title *', 50, 135, 50, 150, 265)
        self.organization_name = self.generate_line(5, 'Organization Name *', 50, 180, 50, 195, 265)
        self.email = self.generate_line(6, 'Email *', 50, 225, 50, 240, 265)
        self.organization_website = self.generate_line(7, 'Organization Website', 50, 270, 50, 285, 265)
        self.phone_number = self.generate_line(8, 'Phone Number', 50, 315, 50, 330)

        collab_label = QLabel('Which of the following collaborative opportunities would\n'
                              'you be interested in? (check all that apply)', self)
        collab_label.move(50, 360)
        self.course_project = self.generate_checkbox(9, 'Course Project', 50, 395)
        self.guest_speaker = self.generate_checkbox(10, 'Guest Speaker', 50, 415)
        self.site_visit = self.generate_checkbox(11, 'Site Vist', 50, 435)
        self.job_shadow = self.generate_checkbox(12, 'Job Shadow', 50, 455)
        self.internships = self.generate_checkbox(13, 'Internships', 50, 475)
        self.career_panel = self.generate_checkbox(14, 'Career Panel', 50, 495)
        self.networking_event = self.generate_checkbox(15, 'Networking Event', 50, 515)

        collab_time_label = QLabel('Your proposed collaboration time period', self)
        collab_time_label.move(50, 540)
        self.summer_2022 = self.generate_checkbox(16, 'Summer 2022 (June 2022- August 2022)', 50, 560)
        self.fall_2022 = self.generate_checkbox(17, 'Fall 2022 (September 2022- December 2022)', 50, 580)
        self.spring_2023 = self.generate_checkbox(18, 'Spring 2023 (January 2023- April 2023)', 50, 600)
        self.summer_2023 = self.generate_checkbox(19, 'Summer 2023 (June 2023- August 2023)', 50, 620)
        self.other_time_period = self.generate_checkbox(20, 'Other', 50, 640)

        self.organization_name_usage = self.generate_line(21, 'If you participate in a CUBEs project, do we have your\n'
                                                              'permission to use your organizations name upon\n'
                                                              'completion, when listing completed projects?',
                                                          50, 665, 50, 715, 265)
        self.show()

    def generate_line(self, field: int, label_text: str, label_x: int, label_y: int, line_x: int, line_y: int, width=None):
        label = QLabel(label_text, self)
        label.move(label_x, label_y)
        line = QLineEdit('', self) if not self.db_entry[field] else QLineEdit(self.db_entry[field], self)
        line.move(line_x, line_y)
        if width:
            line.setFixedWidth(width)
        line.setReadOnly(True)
        return line

    def generate_checkbox(self, field: int, checkbox_text: str, checkbox_x: int, checkbox_y: int):
        checkbox = QCheckBox(checkbox_text, self)
        checkbox.setChecked(True) if self.db_entry[field] == 'Y' else checkbox.setChecked(False)
        checkbox.move(checkbox_x, checkbox_y)
        checkbox.setDisabled(True)
        return checkbox
