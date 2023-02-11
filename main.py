from api_handler import get_entries, save_entries_to_text_file
from db_handler import set_up_db, process_entries_data, save_entries_to_db, close_db, open_db
from gui_handler import display_entries_list


def main():
    url = 'https://mbui.wufoo.com/api/v3/forms/cubes-project-proposal-submission/entries/json'
    # comment to test workflow
    entries = get_entries(url)

    filename = 'cubes_project_proposal_entries.txt'
    save_entries_to_text_file(entries, filename)

    db_name = 'cubes_project_proposal_db.sqlite'
    connection, cursor = set_up_db(db_name)
    entries_data = process_entries_data(entries)
    save_entries_to_db(entries_data, cursor)
    close_db(connection, cursor)

    connection, cursor = open_db(db_name)
    cursor.execute('''SELECT * FROM entries;''')
    db_entries = cursor.fetchall()
    display_entries_list(db_entries)


if __name__ == '__main__':
    main()
