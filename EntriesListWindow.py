from PySide6.QtWidgets import QApplication, QWidget, QListWidget, QListWidgetItem, QPushButton
from PySide6.QtGui import QColor
from EntryDataWindow import EntryDataWindow
from ClaimWindow import ClaimWindow
from db_handler import get_claim_record
from UserDataWindow import UserDataWindow


class EntriesListWindow(QWidget):
    def __init__(self, db_entries, db_filename: str):
        super().__init__()
        self.db_entries = db_entries
        self.db_filename = db_filename
        self.db_entry = None
        self.list_view = None
        self.current = None
        self.selected_list_item = None
        self.entry_data_window = None
        self.claim_window = None
        self.user_data_window = None
        self.claim_record = None
        self.setup()

    def setup(self):
        self.setWindowTitle('CUBES Project Proposal Entries')
        self.setGeometry(0, 0, 500, 500)
        list_view = QListWidget(self)
        self.list_view = list_view
        list_view.resize(500, 455)
        self.put_entries_in_list(self.db_entries)
        list_view.currentItemChanged.connect(self.list_item_selected)
        quit_button = QPushButton('Quit', self)
        quit_button.clicked.connect(QApplication.instance().quit)
        quit_button.resize(quit_button.sizeHint())
        quit_button.move(410, 465)
        self.show()

    def put_entries_in_list(self, db_entries: list[tuple]):
        for db_entry in db_entries:
            list_item_text = f'{db_entry[0]}\t{db_entry[2]}\t{db_entry[3]}\t{db_entry[5]}'
            list_item = QListWidgetItem(list_item_text, listview=self.list_view)
            if self.is_claimed(db_entry):
                list_item.setForeground(QColor('red'))

    def find_complete_entry_data(self, db_entry_id: str):
        for db_entry in self.db_entries:
            if db_entry[0] == int(db_entry_id):
                return db_entry

    def list_item_selected(self, current: QListWidgetItem, previous: QListWidgetItem):
        self.current = current
        self.selected_list_item = current.data(0)
        db_entry_id = self.selected_list_item.split('\t')[0]
        self.db_entry = self.find_complete_entry_data(db_entry_id)
        print(self.db_entry)
        self.entry_data_window = EntryDataWindow(self.db_entry)
        self.entry_data_window.show()
        self.show_claim_or_user_window()

    def is_claimed(self, db_entry: tuple):
        self.claim_record = get_claim_record(self.db_filename, db_entry)
        if len(self.claim_record) == 0:
            print('entry not claimed')
            return False
        else:
            print('entry is claimed')
            return True

    def show_claim_or_user_window(self):
        self.claim_window = ClaimWindow(self.db_entry, self.current, self.db_filename)
        self.user_data_window = UserDataWindow(self.db_entry, self.db_filename)
        if self.is_claimed(self.db_entry):
            self.claim_window.hide()
            self.user_data_window.show()
        else:
            self.claim_window.show()
            self.user_data_window.hide()
