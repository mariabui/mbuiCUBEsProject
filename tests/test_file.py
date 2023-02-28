from api_handler import get_entries
from db_handler import set_up_db, open_db, close_db, create_entries_table, save_entries_to_db, get_entries_from_db
from EntriesListWindow import EntriesListWindow
from PySide6.QtWidgets import QListWidgetItem
from ClaimWindow import ClaimWindow


def test_get_data():
    entries = get_entries('https://mbui.wufoo.com/api/v3/forms/cubes-project-proposal-submission/entries/json')
    assert len(entries) >= 10


def test_create_table():
    connection, cursor = open_db('test_db.sqlite')  # creates a new empty db and runs entries table creation function
    create_entries_table(cursor)
    # verify that the entries table is created properly in the db
    cursor.execute('''SELECT COUNT(*) FROM sqlite_master;''')
    table_count = cursor.fetchone()[0]
    assert table_count == 1  # there is a table in the db
    cursor.execute('''SELECT name FROM sqlite_master WHERE type = 'table';''')
    table_name = cursor.fetchall()[0][0]
    assert table_name == 'entries'  # the table's name is 'entries'
    cursor.execute('''SELECT COUNT(*) FROM sqlite_master WHERE name = 'entries';''')
    entries_table_count = cursor.fetchone()[0]
    assert entries_table_count == 1  # there is an entries table in the db
    cursor.execute('''SELECT COUNT(*) FROM sqlite_master WHERE type = 'table' AND name = 'entries';''')
    assert cursor.fetchone()[0] == 1
    cursor.execute('''SELECT * FROM sqlite_master WHERE tbl_name = 'entries' AND type = 'table';''')
    assert len(cursor.fetchall()) == 1
    close_db(connection, cursor)


def test_save_data_to_db():
    test_entry_data = [
        (15, None, 'Chip', 'Skylark', 'Singer', 'Nickelodeon', 'cskylark@nick.com', None, None, 'N', 'Y', 'Y', 'Y', 'N',
         'N', 'N', 'N', 'N', 'Y', 'Y', 'N', 'Yes', '2023-02-02 17:41:30', 'public')
    ]
    connection, cursor = open_db('test_db.sqlite')
    save_entries_to_db(test_entry_data, cursor)
    close_db(connection, cursor)
    connection, cursor = open_db('test_db.sqlite')
    # verify that the db contains the test entry that was put there
    cursor.execute('''SELECT COUNT(*) FROM entries;''')
    entries_count = cursor.fetchone()[0]
    assert entries_count == 1  # there is an entry saved in the entries table
    cursor.execute('''SELECT * FROM entries;''')
    assert len(cursor.fetchall()) == 1
    cursor.execute('''SELECT * FROM entries WHERE entry_id = 15;''')
    saved_entry = cursor.fetchall()
    assert saved_entry[0] == test_entry_data[0]  # the test entry is saved to the db
    cursor.execute('''SELECT COUNT(*) FROM entries WHERE entry_id = 15;''')
    assert cursor.fetchone()[0] == 1
    cursor.execute('''SELECT first_name FROM entries;''')
    assert cursor.fetchall()[0][0] == 'Chip'
    close_db(connection, cursor)


def test_entry_data_population(qtbot):
    db_filename = 'test_db.sqlite'
    connection, cursor = set_up_db(db_filename)
    close_db(connection, cursor)
    db_entries = get_entries_from_db(db_filename)
    entries_list_window = EntriesListWindow(db_entries, db_filename)
    qtbot.addWidget(entries_list_window)
    list_item = QListWidgetItem('15\tChip\tSkylark\tNickelodeon', listview=entries_list_window.list_view)
    entries_list_window.list_item_selected(list_item, list_item)
    assert entries_list_window.entry_data_window.first_name.text() == 'Chip'
    assert entries_list_window.entry_data_window.last_name.text() == 'Skylark'
    assert entries_list_window.entry_data_window.title.text() == 'Singer'
    assert entries_list_window.entry_data_window.organization_name.text() == 'Nickelodeon'
    assert entries_list_window.entry_data_window.email.text() == 'cskylark@nick.com'
    assert entries_list_window.entry_data_window.course_project.isChecked() is False
    assert entries_list_window.entry_data_window.guest_speaker.isChecked() is True
    assert entries_list_window.entry_data_window.summer_2022.isChecked() is False
    assert entries_list_window.entry_data_window.spring_2023.isChecked() is True


def test_user_creation(qtbot):
    db_filename = 'test_db.sqlite'
    db_entries = get_entries_from_db(db_filename)
    current = QListWidgetItem('15\tChip\tSkylark\tNickelodeon')
    claim_window = ClaimWindow(db_entries[0], current, db_filename)
    qtbot.addWidget(claim_window)
    claim_window.email.setText('jsantore@bridgew.edu')
    claim_window.show_lines_or_fields()
    claim_window.first_name.setText('John')
    claim_window.last_name.setText('Santore')
    claim_window.title.setText('Professor')
    claim_window.department.setText('Computer Science')
    claim_window.claim()
    connection, cursor = open_db(db_filename)
    cursor.execute('''SELECT * FROM users WHERE email = 'jsantore@bridgew.edu';''')
    user_record = cursor.fetchone()
    assert user_record[0] == 'jsantore@bridgew.edu'
    assert user_record[1] == 'John'
    assert user_record[2] == 'Santore'
    assert user_record[3] == 'Professor'
    assert user_record[4] == 'Computer Science'


def test_user_data_population(qtbot):
    db_filename = 'test_db.sqlite'
    db_entries = get_entries_from_db(db_filename)
    current = QListWidgetItem('15\tChip\tSkylark\tNickelodeon')
    claim_window = ClaimWindow(db_entries[0], current, db_filename)
    qtbot.addWidget(claim_window)
    claim_window.email.setText('jsantore@bridgew.edu')
    claim_window.show_lines_or_fields()
    assert claim_window.email.text() == 'jsantore@bridgew.edu'
    assert claim_window.first_name.text() == 'John'
    assert claim_window.last_name.text() == 'Santore'
    assert claim_window.title.text() == 'Professor'
    assert claim_window.department.text() == 'Computer Science'


def test_():
    pass
