import os
from PySide6.QtWidgets import QListWidgetItem
from EntriesListWindow import EntriesListWindow
from ClaimWindow import ClaimWindow
from api_handler import get_entries
from db_handler import set_up_db, open_db, close_db, create_entries_table, save_entries_to_db,\
    get_entries_records_from_db, get_user_record_from_db


def test_get_data():
    entries = get_entries('https://mbui.wufoo.com/api/v3/forms/cubes-project-proposal-submission/entries/json')
    assert len(entries) >= 10


def test_table_creation():
    connection, cursor = open_db('test_db.sqlite')
    create_entries_table(cursor)
    cursor.execute('''SELECT COUNT(*) FROM sqlite_master;''')
    table_count = cursor.fetchone()[0]
    assert table_count == 1
    cursor.execute('''SELECT name FROM sqlite_master WHERE type = 'table';''')
    table_name = cursor.fetchall()[0][0]
    assert table_name == 'entries'
    cursor.execute('''SELECT COUNT(*) FROM sqlite_master WHERE name = 'entries';''')
    entries_table_count = cursor.fetchone()[0]
    assert entries_table_count == 1
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
    cursor.execute('''SELECT COUNT(*) FROM entries;''')
    entries_count = cursor.fetchone()[0]
    assert entries_count == 1
    cursor.execute('''SELECT * FROM entries;''')
    assert len(cursor.fetchall()) == 1
    cursor.execute('''SELECT * FROM entries WHERE entry_id = 15;''')
    saved_entry = cursor.fetchall()
    assert saved_entry[0] == test_entry_data[0]
    cursor.execute('''SELECT COUNT(*) FROM entries WHERE entry_id = 15;''')
    assert cursor.fetchone()[0] == 1
    cursor.execute('''SELECT first_name, last_name, organization_name FROM entries;''')
    entry_record = cursor.fetchall()[0]
    assert entry_record[0] == 'Chip'
    assert entry_record[1] == 'Skylark'
    assert entry_record[2] == 'Nickelodeon'
    close_db(connection, cursor)


def test_entry_data_population(qtbot):
    db_filename = 'test_db.sqlite'
    connection, cursor = set_up_db(db_filename)
    close_db(connection, cursor)
    entries_records = get_entries_records_from_db(db_filename)
    entries_list_window = EntriesListWindow(db_filename, entries_records)
    qtbot.addWidget(entries_list_window)
    current = QListWidgetItem('15\tChip\tSkylark\tNickelodeon', listview=entries_list_window.list_view)
    entries_list_window.list_item_selected(current, current)
    assert entries_list_window.entry_record == (
        15, None, 'Chip', 'Skylark', 'Singer', 'Nickelodeon', 'cskylark@nick.com', None, None, 'N', 'Y', 'Y', 'Y', 'N',
        'N', 'N', 'N', 'N', 'Y', 'Y', 'N', 'Yes', '2023-02-02 17:41:30', 'public'
    )
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
    """
    User creation functionality is implemented in the Claim window.
    When a user claims an entry, their user and claim data is saved to the
    users and claims tables in the database, respectively.
    """
    db_filename = 'test_db.sqlite'
    entries_records = get_entries_records_from_db(db_filename)
    current = QListWidgetItem('15\tChip\tSkylark\tNickelodeon')
    claim_window = ClaimWindow(db_filename, entries_records[0], current)
    qtbot.addWidget(claim_window)
    claim_window.bsu_email.setText('jsantore@bridgew.edu')
    claim_window.show_fields_and_claim_button()  # this method is called when the user submits their bsu email
    assert claim_window.user_exists() is False
    assert claim_window.user_record == []
    user_record = get_user_record_from_db(db_filename, claim_window.bsu_email.text())
    assert len(user_record) == 0
    # the user fills in their own data
    claim_window.first_name.setText('John')
    claim_window.last_name.setText('Santore')
    claim_window.title.setText('Professor')
    claim_window.department.setText('Computer Science')
    claim_window.claim()  # this method saves the user and claim data to the db when the user submits their claim
    assert claim_window.user_exists() is True
    assert claim_window.user_record == [('jsantore@bridgew.edu', 'John', 'Santore', 'Professor', 'Computer Science')]
    user_record = get_user_record_from_db(db_filename, claim_window.bsu_email.text())
    assert len(user_record) == 1
    assert user_record[0][0] == 'jsantore@bridgew.edu'
    assert user_record[0][1] == 'John'
    assert user_record[0][2] == 'Santore'
    assert user_record[0][3] == 'Professor'
    assert user_record[0][4] == 'Computer Science'


def test_existing_user_data_population(qtbot):
    """
    When an existing user submits their bsu email, their user data is autofilled in the Claim window.
    """
    db_filename = 'test_db.sqlite'
    entries_records = get_entries_records_from_db(db_filename)
    current = QListWidgetItem('15\tChip\tSkylark\tNickelodeon')
    claim_window = ClaimWindow(db_filename, entries_records[0], current)
    qtbot.addWidget(claim_window)
    claim_window.bsu_email.setText('jsantore@bridgew.edu')
    assert claim_window.bsu_email.text() == 'jsantore@bridgew.edu'
    assert claim_window.first_name.text() == ''
    assert claim_window.last_name.text() == ''
    assert claim_window.title.text() == ''
    assert claim_window.department.text() == ''
    claim_window.show_fields_and_claim_button()  # existing user submits their bsu email
    assert claim_window.user_exists() is True
    assert claim_window.user_record == [('jsantore@bridgew.edu', 'John', 'Santore', 'Professor', 'Computer Science')]
    # fields are autofilled with the existing user's data
    assert claim_window.first_name.text() == 'John'
    assert claim_window.last_name.text() == 'Santore'
    assert claim_window.title.text() == 'Professor'
    assert claim_window.department.text() == 'Computer Science'


def test_claimer_data_population(qtbot):
    """
    When a claimed entry is selected from the list, both the full CUBEs project data and
    the information about the faculty/user who claimed it are displayed.
    A previous test, 'test_entry_data_population',
    verifies that the correct full CUBEs project data is displayed when selected.
    """
    db_filename = 'test_db.sqlite'
    entries_records = get_entries_records_from_db(db_filename)
    entries_list_window = EntriesListWindow(db_filename, entries_records)
    qtbot.addWidget(entries_list_window)
    current = QListWidgetItem('15\tChip\tSkylark\tNickelodeon', listview=entries_list_window.list_view)
    entries_list_window.list_item_selected(current, current)  # a claimed entry is selected
    assert entries_list_window.entry_is_claimed(entries_records[0]) is True
    assert entries_list_window.claim_record == [(1, 15, 'jsantore@bridgew.edu')]
    assert entries_list_window.entry_data_window.isHidden() is False  # entry data window is shown and displays the entry data
    assert entries_list_window.user_data_window.isHidden() is False  # user data window is shown and displays the user data
    assert entries_list_window.claim_window.isHidden() is True  # claim window is hidden
    assert entries_list_window.user_data_window.user_record == [('jsantore@bridgew.edu', 'John', 'Santore',
                                                                 'Professor', 'Computer Science')]
    assert entries_list_window.user_data_window.bsu_email.text() == 'jsantore@bridgew.edu'
    assert entries_list_window.user_data_window.first_name.text() == 'John'
    assert entries_list_window.user_data_window.last_name.text() == 'Santore'
    assert entries_list_window.user_data_window.title.text() == 'Professor'
    assert entries_list_window.user_data_window.department.text() == 'Computer Science'
    os.remove('test_db.sqlite')  # removes the test db file
