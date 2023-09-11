from data_.database import MyDataBase


class MyRepository(MyDataBase):

    def add_user(self, telegram_id, username, role):
        return self.add_user_sql(telegram_id, username, role)

    def get_user(self, telegram_id):
        return self.get_user_sql(telegram_id)

    def all_candidates(self):
        return self.all_candidates_sql()

    def update_user(self, telegram_id, name, age, city, workflow, sources, verticals, geo, profit, statistic):
        return self.update_user_sql(telegram_id, name, age, city, workflow, sources, verticals, geo, profit, statistic)

    def add_vacancy(self, title, requirements, responsibilities, bonus, contact):
        return self.add_vacancy_sql(title, requirements, responsibilities, bonus, contact)

    def get_vacancy(self, id_vacancy):
        return self.get_vacancy_sql(id_vacancy)

    def all_vacancies(self):
        return self.all_vacancies_sql()

    def delete_vacancy(self, id_vacancy):
        return self.delete_vacancy_sql(id_vacancy)
