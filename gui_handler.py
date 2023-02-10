import sys
from PySide6.QtWidgets import QApplication
from EntriesListWindow import EntriesListWindow


def display_entries_list(entries: list[dict]):
    q_app = QApplication(sys.argv)
    window = EntriesListWindow(entries)
    sys.exit(q_app.exec_())
