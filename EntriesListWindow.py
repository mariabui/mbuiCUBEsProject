from PySide6.QtWidgets import QApplication, QWidget, QListWidget, QListWidgetItem, QPushButton
from EntryDataWindow import EntryDataWindow


class EntriesListWindow(QWidget):
    def __init__(self, db_entries):
        super().__init__()
        self.db_entries = db_entries
        self.db_entry = None
        self.list_view = None
        self.entry_data_window = None
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
            QListWidgetItem(list_item_text, listview=self.list_view)

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
