from get_entries_functions import get_entries


def main():
    url = 'https://mbui.wufoo.com/api/v3/forms/cubes-project-proposal-submission/entries/json'
    entries = get_entries(url)
    print(entries)


if __name__ == '__main__':
    main()
