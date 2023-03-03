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


def create_users_table(cursor: sqlite3.Cursor):
    try:
        cursor.execute('''CREATE TABLE IF NOT EXISTS users(
                       email TEXT PRIMARY KEY,
                       first_name TEXT NOT NULL,
                       last_name TEXT NOT NULL,
                       title TEXT NOT NULL,
                       department TEXT NOT NULL);''')
    except sqlite3.Error as error:
        print(f'Failed to create users table, {error}')
        sys.exit(-1)


def create_claims_table(cursor: sqlite3.Cursor):
    try:
        cursor.execute('''CREATE TABLE IF NOT EXISTS claims(
                       claim_id INTEGER PRIMARY KEY,
                       entry_id INTEGER,
                       email TEXT,
                       FOREIGN KEY (entry_id) REFERENCES entries (entry_id)
                       ON DELETE CASCADE ON UPDATE NO ACTION,
                       FOREIGN KEY (email) REFERENCES users (email)
                       ON DELETE CASCADE ON UPDATE NO ACTION);''')
    except sqlite3.Error as error:
        print(f'Failed to create claims table, {error}')
        sys.exit(-1)


def set_up_db(db_filename: str) -> tuple[sqlite3.Connection, sqlite3.Cursor]:
    connection, cursor = open_db(db_filename)
    create_entries_table(cursor)
    create_users_table(cursor)
    create_claims_table(cursor)
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
        cursor.executemany('''INSERT OR IGNORE INTO entries VALUES(
        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);''', entries_data)
    except sqlite3.Error as error:
        print(f'Failed to save entries to database, {error}')
        sys.exit(-1)


def save_user_to_db(user_data: tuple, cursor: sqlite3.Cursor):
    try:
        cursor.execute('''INSERT OR IGNORE INTO users VALUES(?, ?, ?, ?, ?);''', user_data)
    except sqlite3.Error as error:
        print(f'Failed to save user to database, {error}')
        sys.exit(-1)


def save_claim_to_db(claim_data: tuple, cursor: sqlite3.Cursor):
    try:
        cursor.execute('''INSERT OR IGNORE INTO claims (entry_id, email) VALUES(?, ?);''', claim_data)
    except sqlite3.Error as error:
        print(f'Failed to save claim to database, {error}')
        sys.exit(-1)


def get_entry_records_from_db(db_filename: str) -> list[tuple]:
    connection, cursor = open_db(db_filename)
    cursor.execute('''SELECT * FROM entries;''')
    db_entries = cursor.fetchall()
    close_db(connection, cursor)
    return db_entries


def get_user_record_from_db(db_filename: str, email: str):
    connection, cursor = open_db(db_filename)
    cursor.execute('''SELECT * FROM users WHERE email = ?;''', [email])
    user_record = cursor.fetchall()
    close_db(connection, cursor)
    return user_record


def get_claim_record_from_db(db_filename: str, db_entry: tuple):
    connection, cursor = open_db(db_filename)
    cursor.execute('''SELECT * FROM claims WHERE entry_id = ?;''', [db_entry[0]])
    claim_record = cursor.fetchall()
    close_db(connection, cursor)
    return claim_record
