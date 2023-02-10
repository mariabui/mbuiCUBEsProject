from PySide6.QtWidgets import QApplication, QWidget, QListWidget, QListWidgetItem, QPushButton
from EntryDataWindow import EntryDataWindow


class EntriesListWindow(QWidget):
    def __init__(self, entries):
        super().__init__()
        self.entries = entries
        self.list_window = None
        self.data_window = None
        self.setup()

    def setup(self):
        self.setWindowTitle('CUBES Project Proposal Entries')
        self.setGeometry(0, 0, 450, 500)
        list_window = QListWidget(self)
        self.list_window = list_window
        list_window.resize(450, 460)
        self.put_entries_in_list(self.entries)
        list_window.currentItemChanged.connect(self.list_item_selected)
        quit_button = QPushButton('Quit', self)
        quit_button.clicked.connect(QApplication.instance().quit)
        quit_button.resize(quit_button.sizeHint())
        quit_button.move(380, 470)
        self.show()

    def put_entries_in_list(self, entries: list[dict]):
        for entry in entries:
            list_item_text = f"{entry['EntryId']}\t{entry['Field2']}\t{entry['Field3']}\t{entry['Field5']}"
            # list_item = QListWidgetItem(list_item_text, listview=self.list_window)
            QListWidgetItem(list_item_text, listview=self.list_window)

    def find_complete_entry(self, entry_id: str):
        for entry in self.entries:
            if entry['EntryId'] == entry_id:
                return entry

    def list_item_selected(self, current: QListWidgetItem, previous: QListWidgetItem):
        selected_list_item = current.data(0)
        entry_id = selected_list_item.split('\t')[0]
        entry = self.find_complete_entry(entry_id)
        print(entry)
        self.data_window = EntryDataWindow(entry)
        self.data_window.show()
