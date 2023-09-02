import pymysql as pymysql

from private import DATABASE_PASSWORD, DATABASE_NAME


class Connection:
    def __init__(self):
        self.connection = pymysql.connect(
            host="localhost",
            user="root",
            password=DATABASE_PASSWORD,
            db=DATABASE_NAME,
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor
        )

    def select_all_vacancies(self):
        pass


