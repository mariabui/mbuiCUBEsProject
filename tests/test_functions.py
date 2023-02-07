from api_data import get_entries
from db_handler import open_db, create_entries_table, clear_entries_table, save_entries_to_db, close_db


def test_get_entries():
    entries = get_entries('https://mbui.wufoo.com/api/v3/forms/cubes-project-proposal-submission/entries/json')
    assert len(entries) > 10


def test_create_entries_table_and_save_entries_to_db():
    test_entry = [
        {'EntryId': '15', 'Field1': '', 'Field2': 'Chip', 'Field3': 'Skylark', 'Field4': 'Singer',
         'Field5': 'Nickelodeon', 'Field6': 'cskylark@nick.com', 'Field7': '', 'Field8': '', 'Field9': '',
         'Field10': 'Guest Speaker', 'Field11': 'Site Visit', 'Field12': 'Job Shadow', 'Field13': '', 'Field14': '',
         'Field15': '', 'Field109': '', 'Field110': '', 'Field111': 'Spring 2023 (January 2023- April 2023)',
         'Field112': 'Summer 2023 (June 2023- August 2023)', 'Field113': '', 'Field210': 'Yes',
         'DateCreated': '2023-02-02 17:41:30', 'CreatedBy': 'public', 'DateUpdated': '', 'UpdatedBy': None}
    ]
    connection, cursor = open_db('test.sqlite')
    create_entries_table(cursor)
    clear_entries_table(cursor)
    cursor.execute('''SELECT COUNT(*) FROM sqlite_master;''')
    table_count = cursor.fetchone()[0]
    assert table_count == 1
    cursor.execute('''SELECT name FROM sqlite_master WHERE type = 'table';''')
    table_name = cursor.fetchone()[0]
    assert table_name == 'entries'
    save_entries_to_db(test_entry, cursor)
    cursor.execute('''SELECT * FROM entries;''')
    saved_entries = cursor.fetchall()
    assert saved_entries == [
        (15, None, 'Chip', 'Skylark', 'Singer', 'Nickelodeon', 'cskylark@nick.com', None, None, 'No', 'Yes', 'Yes',
         'Yes', 'No', 'No', 'No', 'No', 'No', 'Yes', 'Yes', 'No', 'Yes', '2023-02-02 17:41:30', 'public')
    ]
    close_db(connection, cursor)
