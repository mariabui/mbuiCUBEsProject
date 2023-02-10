from api_handler import get_entries, save_entries_to_text_file
from db_handler import set_up_db, process_entries_data, save_entries_to_db, close_db
from gui_handler import display_entries_list


def main():
    url = 'https://mbui.wufoo.com/api/v3/forms/cubes-project-proposal-submission/entries/json'
    # comment to test workflow
    entries = get_entries(url)

    # filename = 'cubes_project_proposal_entries.txt'
    # save_entries_to_text_file(entries, filename)
    #
    # connection, cursor = set_up_db('cubes_project_proposal_db.sqlite')
    # entries_data = process_entries_data(entries)
    # save_entries_to_db(entries_data, cursor)
    # close_db(connection, cursor)

    display_entries_list(entries)


if __name__ == '__main__':
    main()
