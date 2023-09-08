from data_.database import MyDataBase


class MyRepository(MyDataBase):

    def add_user(self, telegram_id, username, role):
        return self.add_user_sql(telegram_id, username, role)

    def get_user(self, telegram_id):
        return self.get_user_sql(telegram_id)

    def add_vacancy(self, title, desc):
        return self.add_vacancy_sql(title, desc)

    def all_vacancies(self):
        return self.all_vacancies_sql()
