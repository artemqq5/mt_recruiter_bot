import pymysql

from private import DATABASE_PASSWORD, DATABASE_NAME


class MyDataBase:
    def __init__(self):
        self.connection = pymysql.connect(
            host="localhost",
            user="root",
            password=DATABASE_PASSWORD,
            db=DATABASE_NAME,
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor
        )

    def add_user_sql(self, telegram_id, username, role):
        try:
            with self.connection as connection:
                with connection.cursor() as cursor:
                    _command = f'''INSERT INTO `users` (`telegram_id`, `username`, `role`) VALUES (%s, %s, %s);'''

                    cursor.execute(_command, (telegram_id, username, role))
                    result = cursor.fetchall()

                connection.commit()
                return result
        except Exception as e:
            print(f"add_user_sql: {e}")
            return None

    def get_user_sql(self, telegram_id):
        try:
            with self.connection as connection:
                with connection.cursor() as cursor:
                    _command = f'''SELECT * FROM `users` WHERE `telegram_id` = %s;'''

                    cursor.execute(_command, (telegram_id,))
                    result = cursor.fetchall()[0]

                connection.commit()
                return result
        except Exception as e:
            print(f"add_user_sql: {e}")
            return None

    def add_vacancy_sql(self, title, desc):
        try:
            with self.connection as connection:
                with connection.cursor() as cursor:
                    _command = f'''INSERT INTO `vacancies` (`title`, `desc`) VALUES (%s, %s);'''
                    cursor.execute(_command, (title, desc))

                connection.commit()
                return cursor.lastrowid
        except Exception as e:
            print(f"add_vacancy_sql: {e}")
            return None

    def all_vacancies_sql(self):
        try:
            with self.connection as connection:
                with connection.cursor() as cursor:
                    _command = f'''SELECT * FROM `vacancies`;'''
                    cursor.execute(_command)
                    result = cursor.fetchall()

                connection.commit()
                return result
        except Exception as e:
            print(f"all_vacancies_sql: {e}")
            return None

    # def delete_vacancy_sql(self, id_vacancy):
    #     try:
    #         with self.connection as connection:
    #             with connection.cursor() as cursor:
    #                 _command = f"""DELETE FROM `{TABLE_VACANCIES}` WHERE `id` = '{id_vacancy}');"""
    #                 cursor.execute(_command)
    #                 result = cursor.fetchall()
    #
    #             connection.commit()
    #             return result
    #     except Exception as e:
    #         print(f"delete_vacancy_sql: {e}")
    #         return None
