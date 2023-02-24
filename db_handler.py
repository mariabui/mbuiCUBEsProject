import sys
import sqlite3


def open_db(db_filename: str) -> tuple[sqlite3.Connection, sqlite3.Cursor]:
    try:
        connection = sqlite3.connect(db_filename)
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


def create_entries_table(cursor: sqlite3.Cursor):
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
                       other_time_period TEXT,
                       organization_name_usage TEXT,
                       date_created TEXT,
                       created_by TEXT);''')
    except sqlite3.Error as error:
        print(f'Failed to create entries table, {error}')
        sys.exit(-1)


def clear_entries_table(cursor: sqlite3.Cursor):
    try:
        cursor.execute('''DELETE FROM entries;''')
    except sqlite3.Error as error:
        print(f'Failed to clear entries table, {error}')
        sys.exit(-1)


def create_faculties_table(cursor: sqlite3.Cursor):
    try:
        cursor.execute('''CREATE TABLE IF NOT EXISTS faculties(
                       email TEXT PRIMARY KEY,
                       first_name TEXT NOT NULL,
                       last_name TEXT NOT NULL,
                       title TEXT NOT NULL,
                       department TEXT);''')
    except sqlite3.Error as error:
        print(f'Failed to create faculties table, {error}')
        sys.exit(-1)


def clear_faculties_table(cursor: sqlite3.Cursor):
    try:
        cursor.execute('''DELETE FROM faculties;''')
    except sqlite3.Error as error:
        print(f'Failed to clear faculties table, {error}')
        sys.exit(-1)


def create_claims_table(cursor: sqlite3.Cursor):
    try:
        cursor.execute('''CREATE TABLE IF NOT EXISTS claims(
                       entry_id INTEGER,
                       email TEXT,
                       FOREIGN KEY (entry_id) REFERENCES entries (entry_id),
                       FOREIGN KEY (email) REFERENCES faculties (email));''')
    except sqlite3.Error as error:
        print(f'Failed to create claims table, {error}')
        sys.exit(-1)


def clear_claims_table(cursor: sqlite3.Cursor):
    try:
        cursor.execute('''DELETE FROM claims;''')
    except sqlite3.Error as error:
        print(f'Failed to clear claims table, {error}')
        sys.exit(-1)


def set_up_db(db_filename: str) -> tuple[sqlite3.Connection, sqlite3.Cursor]:
    connection, cursor = open_db(db_filename)
    create_entries_table(cursor)
    create_faculties_table(cursor)
    create_claims_table(cursor)
    # clear_entries_table(cursor)
    return connection, cursor


def process_entries_data(entries: list[dict]) -> list[tuple]:
    entries_data = []
    for entry in entries:
        entry_values = list(entry.values())[:24]
        entry_values[0] = int(entry_values[0])
        for field in [1, 7, 8]:
            entry_values[field] = None if entry_values[field] == '' else entry_values[field]
        for field in range(9, 21):
            entry_values[field] = 'N' if entry_values[field] == '' else 'Y'
        entries_data.append(tuple(entry_values))
    return entries_data


def save_entries_to_db(entries_data: list[tuple], cursor: sqlite3.Cursor):
    try:
        cursor.executemany('''INSERT INTO entries VALUES(
        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);''', entries_data)
    except sqlite3.Error as error:
        print(f'Failed to save entries to database, {error}')
        sys.exit(-1)


def get_entries_from_db(db_filename: str) -> list[tuple]:
    connection, cursor = open_db(db_filename)
    cursor.execute('''SELECT * FROM entries;''')
    db_entries = cursor.fetchall()
    close_db(connection, cursor)
    return db_entries
