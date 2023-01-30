from api_data import get_entries, save_entries_to_text_file


def main():
    url = 'https://mbui.wufoo.com/api/v3/forms/cubes-project-proposal-submission/entries/json'
    entries = get_entries(url)

    filename = 'cubes_project_proposal_submissions.txt'
    save_entries_to_text_file(entries, filename)


if __name__ == '__main__':
    main()
