import sys
from PySide6.QtWidgets import QApplication
from UpdateOrRunWindow import UpdateOrRunWindow


def update_or_run(db_filename: str):
    q_app = QApplication(sys.argv)
    update_or_run_window = UpdateOrRunWindow(db_filename)
    update_or_run_window.show()
    sys.exit(q_app.exec_())
