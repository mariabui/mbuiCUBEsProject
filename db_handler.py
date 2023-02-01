import sys
import sqlite3


def open_db(db_name: str) -> tuple[sqlite3.Connection, sqlite3.Cursor]:
    try:
        connection = sqlite3.connect(db_name)
        cursor = connection.cursor()
        return connection, cursor
    except sqlite3.Error as error:
        print(f'Failed to open database, {error}')
        sys.exit(-1)


def close_db(connection: sqlite3.Connection, cursor: sqlite3.Cursor):
    try:
        connection.commit()
        cursor.close()
        connection.close()
    except sqlite3.Error as error:
        print(f'Failed to close database, {error}')
        sys.exit(-1)


def create_table(cursor: sqlite3.Cursor):
    try:
        cursor.execute('''CREATE TABLE IF NOT EXISTS entries(
                       entry_id INTEGER PRIMARY KEY,
                       prefix TEXT,
                       first_name TEXT NOT NULL,
                       last_name TEXT NOT NULL,
                       title TEXT NOT NULL,
                       organization_name TEXT NOT NULL,
                       email TEXT NOT NULL,
                       organization_website TEXT,
                       phone_number TEXT,
                       course_project TEXT,
                       guest_speaker TEXT,
                       site_visit TEXT,
                       job_shadow TEXT,
                       internships TEXT,
                       career_panel TEXT,
                       networking_event TEXT,
                       summer_2022 TEXT,
                       fall_2022 TEXT,
                       spring_2023 TEXT,
                       summer_2023 TEXT,
                       other TEXT,
                       organizations_name_usage TEXT,
                       date_created TEXT);''')
    except sqlite3.Error as error:
        print(f'Failed to create table, {error}')
        sys.exit(-1)


def clear_table(cursor: sqlite3.Cursor):
    try:
        cursor.execute('''DELETE FROM entries''')
    except sqlite3.Error as error:
        print(f'Failed to clear table, {error}')
        sys.exit(-1)


def set_up_db(db_name: str) -> tuple[sqlite3.Connection, sqlite3.Cursor]:
    connection, cursor = open_db(db_name)
    create_table(cursor)
    clear_table(cursor)
    return connection, cursor


def convert_entries_to_list_of_tuples(entries: list[dict]) -> list[tuple]:
    entries_list_of_tuples = []
    for entry in entries:
        entry_data = (entry.get('EntryId'),
                      entry['Field1'] if entry['Field1'] != '' else None,
                      entry['Field2'],
                      entry['Field3'],
                      entry['Field4'],
                      entry['Field5'],
                      entry['Field6'],
                      entry['Field7'] if entry['Field7'] != '' else None,
                      entry['Field8'] if entry['Field8'] != '' else None,
                      'Yes' if entry['Field9'] != '' else 'No',
                      'Yes' if entry['Field10'] != '' else 'No',
                      'Yes' if entry['Field11'] != '' else 'No',
                      'Yes' if entry['Field12'] != '' else 'No',
                      'Yes' if entry['Field13'] != '' else 'No',
                      'Yes' if entry['Field14'] != '' else 'No',
                      'Yes' if entry['Field15'] != '' else 'No',
                      'Yes' if entry['Field109'] != '' else 'No',
                      'Yes' if entry['Field110'] != '' else 'No',
                      'Yes' if entry['Field111'] != '' else 'No',
                      'Yes' if entry['Field112'] != '' else 'No',
                      'Yes' if entry['Field113'] != '' else 'No',
                      entry.get('Field210'),
                      entry.get('DateCreated'))
        entries_list_of_tuples.append(entry_data)
    return entries_list_of_tuples


def save_entries_to_db(entries: list[dict], cursor: sqlite3.Cursor):
    entries_list_of_tuples = convert_entries_to_list_of_tuples(entries)
    try:
        cursor.executemany('INSERT INTO entries VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', entries_list_of_tuples)
    except sqlite3.Error as error:
        print(f'Failed to save entries to database, {error}')
        sys.exit(-1)
