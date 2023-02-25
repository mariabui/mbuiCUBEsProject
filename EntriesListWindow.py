from PySide6.QtWidgets import QApplication, QWidget, QListWidget, QListWidgetItem, QPushButton
from PySide6.QtGui import QColor
from EntryDataWindow import EntryDataWindow
from ClaimWindow import ClaimWindow
from db_handler import get_entry_from_db


class EntriesListWindow(QWidget):
    def __init__(self, db_entries):
        super().__init__()
        self.db_entries = db_entries
        self.db_entry = None
        self.list_view = None
        self.entry_data_window = None
        self.claim_window = None
        # self.claim_button = None
        self.setup()

    def setup(self):
        self.setWindowTitle('CUBES Project Proposal Entries')
        self.setGeometry(0, 0, 500, 500)
        list_view = QListWidget(self)
        self.list_view = list_view
        list_view.resize(500, 470)
        self.put_entries_in_list(self.db_entries)
        list_view.currentItemChanged.connect(self.list_item_selected)
        quit_button = QPushButton('Quit', self)
        quit_button.clicked.connect(QApplication.instance().quit)
        quit_button.resize(quit_button.sizeHint())
        quit_button.move(440, 470)
        # self.claim_button = QPushButton('Claim', self)
        # self.claim_button.clicked.connect(self.claim)
        # self.claim_button.resize(self.claim_button.sizeHint())
        # self.claim_button.move(220, 470)
        self.show()

    def put_entries_in_list(self, db_entries: list[tuple]):
        for db_entry in db_entries:
            list_item_text = f'{db_entry[0]}\t{db_entry[2]}\t{db_entry[3]}\t{db_entry[5]}'
            list_item = QListWidgetItem(list_item_text, listview=self.list_view)
            # self.check_entry_claimed(db_entry)
            # print(db_entry)
            if self.check_entry_claimed(db_entry):
                list_item.setForeground(QColor('red'))

    def find_complete_entry_data(self, db_entry_id: str):
        for db_entry in self.db_entries:
            if db_entry[0] == int(db_entry_id):
                return db_entry

    def list_item_selected(self, current: QListWidgetItem, previous: QListWidgetItem):
        selected_list_item = current.data(0)
        db_entry_id = selected_list_item.split('\t')[0]
        self.db_entry = self.find_complete_entry_data(db_entry_id)
        print(self.db_entry)
        self.entry_data_window = EntryDataWindow(self.db_entry)
        self.entry_data_window.show()
        # self.check_entry_claimed(self.db_entry)
        self.show_or_hide_claim_window(self.db_entry)

    # def claim(self):
        # self.claim_window = ClaimWindow(self.db_entry)
        # self.claim_window.show()

    def check_entry_claimed(self, db_entry: tuple):
        entry_record = get_entry_from_db('cubes_db.sqlite', db_entry[0])
        if len(entry_record) == 0:
            print('entry not claimed')
            return False
        else:
            print('entry claimed')
            return True

    def show_or_hide_claim_window(self, db_entry: tuple):
        self.claim_window = ClaimWindow(self.db_entry)
        claimed = self.check_entry_claimed(db_entry)
        if claimed:
            self.claim_window.hide()
            # self.claim_button.setDisabled(False)
        else:
            self.claim_window.show()
            # self.claim_button.setDisabled(True)
