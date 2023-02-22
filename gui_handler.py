import sys
from PySide6.QtWidgets import QApplication
from EntriesListWindow import EntriesListWindow


def display_entries_in_gui(db_entries: list[tuple]):
    q_app = QApplication(sys.argv)
    entries_list_window = EntriesListWindow(db_entries)
    entries_list_window.show()
    sys.exit(q_app.exec_())
