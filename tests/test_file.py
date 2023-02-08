from api_data import get_entries
from db_handler import set_up_db, save_entries_to_db, close_db, open_db


def test_get_data_from_internet():
    entries = get_entries('https://mbui.wufoo.com/api/v3/forms/cubes-project-proposal-submission/entries/json')
    assert len(entries) > 10  # the right number of data items retrieved is more than 10


def test_data_goes_into_db():
    test_entry = [
        {'EntryId': '15', 'Field1': '', 'Field2': 'Chip', 'Field3': 'Skylark', 'Field4': 'Singer',
         'Field5': 'Nickelodeon', 'Field6': 'cskylark@nick.com', 'Field7': '', 'Field8': '', 'Field9': '',
         'Field10': 'Guest Speaker', 'Field11': 'Site Visit', 'Field12': 'Job Shadow', 'Field13': '', 'Field14': '',
         'Field15': '', 'Field109': '', 'Field110': '', 'Field111': 'Spring 2023 (January 2023- April 2023)',
         'Field112': 'Summer 2023 (June 2023- August 2023)', 'Field113': '', 'Field210': 'Yes',
         'DateCreated': '2023-02-02 17:41:30', 'CreatedBy': 'public', 'DateUpdated': '', 'UpdatedBy': None}
    ]
    connection, cursor = set_up_db('test_db.sqlite')  # creates a new empty db and runs entries table creation function
    save_entries_to_db(test_entry, cursor)
    close_db(connection, cursor)

    connection, cursor = open_db('test_db.sqlite')
    # verify that the entries table is created properly in the db
    cursor.execute('''SELECT COUNT(*) FROM sqlite_master;''')
    table_count = cursor.fetchall()[0][0]
    assert table_count == 1  # there is a table in the db
    cursor.execute('''SELECT name FROM sqlite_master WHERE type = 'table';''')
    table_name = cursor.fetchall()[0][0]
    assert table_name == 'entries'  # the table's name is 'entries'
    cursor.execute('''SELECT COUNT(*) FROM sqlite_master WHERE name = 'entries';''')
    entries_table_count = cursor.fetchall()[0][0]
    assert entries_table_count == 1  # there is an entries table in the db

    # verify that the db contains the test entry that was put there
    cursor.execute('''SELECT * FROM entries;''')
    saved_entries = cursor.fetchall()
    assert len(saved_entries) == 1  # there is an entry saved in the entries table
    assert saved_entries == [
        (15, None, 'Chip', 'Skylark', 'Singer', 'Nickelodeon', 'cskylark@nick.com', None, None, 'No', 'Yes', 'Yes',
         'Yes', 'No', 'No', 'No', 'No', 'No', 'Yes', 'Yes', 'No', 'Yes', '2023-02-02 17:41:30', 'public')
    ]  # the test entry is saved to the db
    cursor.execute('''SELECT entry_id FROM entries;''')
    saved_entry_id = cursor.fetchall()[0][0]
    assert saved_entry_id == 15  # the test entry's id is 15
    close_db(connection, cursor)
