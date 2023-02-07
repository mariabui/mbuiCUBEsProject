from api_data import get_entries
from db_handler import set_up_db, open_db, save_entries_to_db, close_db


def test_get_entries():
    entries = get_entries('https://mbui.wufoo.com/api/v3/forms/cubes-project-proposal-submission/entries/json')
    assert len(entries) > 10  # the right number of data items retrieved should be more than 10


def test_set_up_db_and_save_entries_to_db():
    test_entry = [
        {'EntryId': '15', 'Field1': '', 'Field2': 'Chip', 'Field3': 'Skylark', 'Field4': 'Singer',
         'Field5': 'Nickelodeon', 'Field6': 'cskylark@nick.com', 'Field7': '', 'Field8': '', 'Field9': '',
         'Field10': 'Guest Speaker', 'Field11': 'Site Visit', 'Field12': 'Job Shadow', 'Field13': '', 'Field14': '',
         'Field15': '', 'Field109': '', 'Field110': '', 'Field111': 'Spring 2023 (January 2023- April 2023)',
         'Field112': 'Summer 2023 (June 2023- August 2023)', 'Field113': '', 'Field210': 'Yes',
         'DateCreated': '2023-02-02 17:41:30', 'CreatedBy': 'public', 'DateUpdated': '', 'UpdatedBy': None}
    ]
    connection, cursor = set_up_db('test.sqlite')
    save_entries_to_db(test_entry, cursor)
    close_db(connection, cursor)

    connection, cursor = open_db('test.sqlite')
    # verify that the entries table is created properly in the database
    cursor.execute('''SELECT COUNT(*) FROM sqlite_master WHERE name = 'entries';''')
    table_count = cursor.fetchall()[0][0]
    assert table_count == 1  # there should be a table created and named 'entries'
    cursor.execute('''SELECT name FROM sqlite_master WHERE type = 'table';''')
    table_name = cursor.fetchall()[0][0]
    assert table_name == 'entries'  # the table created should have the name 'entries'

    # verify that the database contains the test entry put there
    cursor.execute('''SELECT * FROM entries;''')
    saved_entries = cursor.fetchall()
    assert len(saved_entries) == 1  # there should be an entry saved in the entries table
    assert saved_entries == [
        (15, None, 'Chip', 'Skylark', 'Singer', 'Nickelodeon', 'cskylark@nick.com', None, None, 'No', 'Yes', 'Yes',
         'Yes', 'No', 'No', 'No', 'No', 'No', 'Yes', 'Yes', 'No', 'Yes', '2023-02-02 17:41:30', 'public')
    ]  # the saved entry should match the test entry data
    saved_entry_id = saved_entries[0][0]
    assert saved_entry_id == 15  # the saved entry should have an entry_id of 15
    close_db(connection, cursor)
