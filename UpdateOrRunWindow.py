from PySide6.QtWidgets import QWidget, QLabel, QPushButton
from api_handler import get_entries
from db_handler import open_db, close_db, clear_entries_table, process_entries_data,\
    save_entries_to_entries_table, get_entries_from_entries_table
from EntriesListWindow import EntriesListWindow


class UpdateOrRunWindow(QWidget):
    def __init__(self, db_filename: str):
        super().__init__()
        self.db_filename = db_filename
        self.db_entries = None
        self.entries_list_window = None
        self.setup()

    def setup(self):
        self.setWindowTitle('CUBES Project')
        label = QLabel('Choose one:', self)
        label.move(95, 50)
        update_button = QPushButton('Update data in database', self)
        update_button.clicked.connect(self.update_db)
        update_button.resize(update_button.sizeHint())
        update_button.move(50, 70)
        run_button = QPushButton('Run data visualization', self)
        run_button.clicked.connect(self.run)
        run_button.resize(update_button.sizeHint())
        run_button.move(50, 100)
        self.show()

    def update_db(self):
        print('user chose to update db')
        entries = get_entries('https://mbui.wufoo.com/api/v3/forms/cubes-project-proposal-submission/entries/json')
        connection, cursor = open_db(self.db_filename)
        clear_entries_table(cursor)
        entries_data = process_entries_data(entries)
        save_entries_to_entries_table(entries_data, cursor)
        close_db(connection, cursor)
        self.db_entries = get_entries_from_entries_table(self.db_filename)
        self.show_entries_list_window()

    def run(self):
        print('user chose to run visual')
        self.db_entries = get_entries_from_entries_table(self.db_filename)
        self.show_entries_list_window()

    def show_entries_list_window(self):
        print('showing entries list window, hide update/run window')
        self.entries_list_window = EntriesListWindow(self.db_entries, self.db_filename)
        self.entries_list_window.show()
        self.hide()
