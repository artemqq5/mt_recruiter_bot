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
                connection.commit()
                return cursor.lastrowid
        except Exception as e:
            print(f"add_user_sql: {e}")
            return None

    def get_user_sql(self, telegram_id):
        try:
            with self.connection as connection:
                with connection.cursor() as cursor:
                    _command = f'''SELECT * FROM `users` WHERE `telegram_id` = %s;'''
                    cursor.execute(_command, (telegram_id,))
                connection.commit()
                return cursor.fetchall()[0]
        except Exception as e:
            print(f"get_user_sql: {e}")
            return None

    def all_candidates_sql(self):
        try:
            with self.connection as connection:
                with connection.cursor() as cursor:
                    _command = f'''SELECT * FROM `users` WHERE `role` = %s;'''
                    cursor.execute(_command, ('user', ))
                connection.commit()
                return cursor.fetchall()
        except Exception as e:
            print(f"all_resume_sql: {e}")
            return None

    def update_user_sql(self, telegram_id, name, age, city, workflow, sources, verticals, geo, profit, statistic):
        try:
            with self.connection as connection:
                with connection.cursor() as cursor:
                    _command = f'''UPDATE `users` SET `name` = %s, `age` = %s, `city` = %s, `workflow` = %s, `sources` = %s, `verticals` = %s, `geo` = %s, `profit` = %s, `statistic` = %s WHERE `telegram_id` = %s;'''
                    cursor.execute(_command, (name, age, city, workflow, sources, verticals, geo, profit, statistic,
                                              telegram_id))
                connection.commit()
                return cursor.lastrowid > 0
        except Exception as e:
            print(f"update_user_sql: {e}")
            return None

    def add_vacancy_sql(self, title, requirements, responsibilities, bonus, contact):
        try:
            with self.connection as connection:
                with connection.cursor() as cursor:
                    _command = f'''INSERT INTO `vacancies` (`title`, `requirements`, `responsibilities`, `bonus`, `contact`) VALUES (%s, %s, %s, %s, %s);'''
                    cursor.execute(_command, (title, requirements, responsibilities, bonus, contact))
                connection.commit()
                return cursor.lastrowid
        except Exception as e:
            print(f"add_vacancy_sql: {e}")
            return None

    def get_vacancy_sql(self, id_vacancy):
        try:
            with self.connection as connection:
                with connection.cursor() as cursor:
                    _command = f'''SELECT * FROM `vacancies` WHERE `id` = %s;'''
                    cursor.execute(_command, (id_vacancy,))
                connection.commit()
                return cursor.fetchall()[0]
        except Exception as e:
            print(f"get_vacancy_sql: {e}")
            return None

    def all_vacancies_sql(self):
        try:
            with self.connection as connection:
                with connection.cursor() as cursor:
                    _command = f'''SELECT * FROM `vacancies`;'''
                    cursor.execute(_command)
                connection.commit()
                return cursor.fetchall()
        except Exception as e:
            print(f"all_vacancies_sql: {e}")
            return None

    def delete_vacancy_sql(self, id_vacancy):
        try:
            with self.connection as connection:
                with connection.cursor() as cursor:
                    _command = f'''DELETE FROM `vacancies` WHERE `id` = %s;'''
                    cursor.execute(_command, (id_vacancy,))
                connection.commit()
                return cursor.lastrowid
        except Exception as e:
            print(f"delete_vacancy_sql: {e}")
            return None
