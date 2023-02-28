from db_handler import set_up_db, close_db
from gui_handler import update_or_run


def main():
    db_filename = 'cubes_db.sqlite'
    connection, cursor = set_up_db(db_filename)
    close_db(connection, cursor)

    update_or_run(db_filename)


if __name__ == '__main__':
    main()
