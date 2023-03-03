import os
from api_handler import get_entries
from db_handler import set_up_db, open_db, close_db, create_entries_table, save_entries_to_db,\
    get_entry_records_from_db, get_user_record_from_db
from EntriesListWindow import EntriesListWindow
from PySide6.QtWidgets import QListWidgetItem
from ClaimWindow import ClaimWindow


def test_get_data():
    entries = get_entries('https://mbui.wufoo.com/api/v3/forms/cubes-project-proposal-submission/entries/json')
    assert len(entries) >= 10


def test_table_creation():
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
    db_entries = get_entry_records_from_db(db_filename)
    entries_list_window = EntriesListWindow(db_filename, db_entries)
    qtbot.addWidget(entries_list_window)
    current = QListWidgetItem('15\tChip\tSkylark\tNickelodeon', listview=entries_list_window.list_view)
    entries_list_window.list_item_selected(current, current)
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
    When a new user claims an entry, their user data is saved to the users table in the database.
    """
    db_filename = 'test_db.sqlite'
    db_entries = get_entry_records_from_db(db_filename)
    current = QListWidgetItem('15\tChip\tSkylark\tNickelodeon')
    claim_window = ClaimWindow(db_filename, db_entries[0], current)
    qtbot.addWidget(claim_window)
    claim_window.email.setText('jsantore@bridgew.edu')
    claim_window.show_fields()  # this method is called when the user submits their email
    assert claim_window.user_exists() is False
    assert claim_window.user_record == []
    # the user fills in their own data
    claim_window.first_name.setText('John')
    claim_window.last_name.setText('Santore')
    claim_window.title.setText('Professor')
    claim_window.department.setText('Computer Science')
    claim_window.claim()  # this method saves the new user data into the db along with their claim
    assert claim_window.user_exists() is True
    assert claim_window.user_record == [('jsantore@bridgew.edu', 'John', 'Santore', 'Professor', 'Computer Science')]
    user_record = get_user_record_from_db(db_filename, claim_window.email.text())
    assert len(user_record) == 1
    assert user_record[0][0] == 'jsantore@bridgew.edu'
    assert user_record[0][1] == 'John'
    assert user_record[0][2] == 'Santore'
    assert user_record[0][3] == 'Professor'
    assert user_record[0][4] == 'Computer Science'


def test_existing_user_data_population(qtbot):
    """
    When an existing user enters their email to submit a claim, the claim window autofills their user data.
    """
    db_filename = 'test_db.sqlite'
    db_entries = get_entry_records_from_db(db_filename)
    current = QListWidgetItem('15\tChip\tSkylark\tNickelodeon')
    claim_window = ClaimWindow(db_filename, db_entries[0], current)
    qtbot.addWidget(claim_window)
    claim_window.email.setText('jsantore@bridgew.edu')
    claim_window.show_fields()  # existing user submits their email
    assert claim_window.user_exists() is True
    assert claim_window.user_record == [('jsantore@bridgew.edu', 'John', 'Santore', 'Professor', 'Computer Science')]
    # fields are autofilled with the ir existing user's data
    assert claim_window.email.text() == 'jsantore@bridgew.edu'
    assert claim_window.first_name.text() == 'John'
    assert claim_window.last_name.text() == 'Santore'
    assert claim_window.title.text() == 'Professor'
    assert claim_window.department.text() == 'Computer Science'


def test_claimer_data_population(qtbot):
    """
    When a claimed entry (project) from the list is selected, both the full CUBEs project data and
    the information about the faculty/user who claimed it are displayed.
    A previous test ('test_entry_data_population') verifies that the selected CUBEs project data is displayed.
    """
    db_filename = 'test_db.sqlite'
    db_entries = get_entry_records_from_db(db_filename)
    entries_list_window = EntriesListWindow(db_filename, db_entries)
    qtbot.addWidget(entries_list_window)
    current = QListWidgetItem('15\tChip\tSkylark\tNickelodeon', listview=entries_list_window.list_view)
    entries_list_window.list_item_selected(current, current)  # a claimed project is selected
    assert entries_list_window.entry_is_claimed(db_entries[0]) is True
    assert entries_list_window.user_data_window.isHidden() is False  # user data window is shown and displays user data
    assert entries_list_window.claim_window.isHidden() is True  # claim window is hidden
    assert entries_list_window.entry_data_window.isHidden() is False  # entry data window is shown and displays entry data
    assert entries_list_window.user_data_window.user_record == [('jsantore@bridgew.edu', 'John', 'Santore',
                                                                 'Professor', 'Computer Science')]
    assert entries_list_window.user_data_window.email.text() == 'jsantore@bridgew.edu'
    assert entries_list_window.user_data_window.first_name.text() == 'John'
    assert entries_list_window.user_data_window.last_name.text() == 'Santore'
    assert entries_list_window.user_data_window.title.text() == 'Professor'
    assert entries_list_window.user_data_window.department.text() == 'Computer Science'
    os.remove('test_db.sqlite')
