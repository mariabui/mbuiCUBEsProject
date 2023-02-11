import sys
from PySide6.QtWidgets import QApplication
from EntriesListWindow import EntriesListWindow


def display_entries_list(db_entries: list[tuple]):
    q_app = QApplication(sys.argv)
    window = EntriesListWindow(db_entries)
    window.show()
    sys.exit(q_app.exec_())
