from PySide6.QtWidgets import QApplication, QWidget, QListWidget, QListWidgetItem, QPushButton
from PySide6.QtGui import QColor
from EntryDataWindow import EntryDataWindow
from ClaimWindow import ClaimWindow
from UserDataWindow import UserDataWindow
from db_handler import get_claim_record_from_db


class EntriesListWindow(QWidget):
    def __init__(self, db_filename: str, entries_records: list[tuple]):
        super().__init__()
        self.db_filename = db_filename
        self.entries_records = entries_records
        self.list_view = None
        self.selected_list_item = None
        self.selected_list_item_data = None
        self.entry_data_window = None
        self.claim_window = None
        self.user_data_window = None
        self.entry_record = None
        self.claim_record = None
        self.setup()

    def setup(self):
        self.setWindowTitle('CUBES Project Proposal Entries')
        self.setGeometry(0, 0, 500, 500)
        self.list_view = QListWidget(self)
        self.list_view.resize(500, 455)
        self.put_entries_in_list(self.entries_records)
        self.list_view.currentItemChanged.connect(self.list_item_selected)
        quit_button = QPushButton('Quit', self)
        quit_button.clicked.connect(QApplication.instance().quit)
        quit_button.resize(quit_button.sizeHint())
        quit_button.move(410, 465)
        self.show()

    def put_entries_in_list(self, entries_records: list[tuple]):
        for entry_record in entries_records:
            list_item_text = f'{entry_record[0]}\t{entry_record[2]}\t{entry_record[3]}\t{entry_record[5]}'
            list_item = QListWidgetItem(list_item_text, listview=self.list_view)
            if self.entry_is_claimed(entry_record):
                list_item.setForeground(QColor('darkRed'))

    def get_complete_entry_record(self, entry_record_id: str):
        for entry_record in self.entries_records:
            if entry_record[0] == int(entry_record_id):
                return entry_record

    def list_item_selected(self, current: QListWidgetItem, previous: QListWidgetItem):
        self.selected_list_item = current
        self.selected_list_item_data = current.data(0)
        entry_record_id = self.selected_list_item_data.split('\t')[0]
        self.entry_record = self.get_complete_entry_record(entry_record_id)
        print(self.entry_record)
        self.entry_data_window = EntryDataWindow(self.entry_record)
        self.entry_data_window.show()
        self.show_claim_or_user_data_window()

    def entry_is_claimed(self, entry_record: tuple):
        self.claim_record = get_claim_record_from_db(self.db_filename, entry_record[0])
        if len(self.claim_record) == 0:
            return False
        else:
            return True

    def show_claim_or_user_data_window(self):
        self.claim_window = ClaimWindow(self.db_filename, self.entry_record, self.selected_list_item)
        self.user_data_window = UserDataWindow(self.db_filename, self.entry_record)
        if self.entry_is_claimed(self.entry_record):
            self.claim_window.hide()
            self.user_data_window.show()
        else:
            self.claim_window.show()
            self.user_data_window.hide()
