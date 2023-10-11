import psycopg2 as psycopg2


class DBManager:

    @classmethod
    def get_companies_and_vacancies_count(cls, database_name, params):
        """
        Получает список всех компаний и количество вакансий у каждой компании
        """
        conn = psycopg2.connect(dbname=database_name, **params)

        with conn.cursor() as cur:
            cur.execute("SELECT * FROM companies")
            rows = cur.fetchall()
            for row in rows:
                cur.execute(f"""select COUNT(*) from vacancies
                                where employer_id = {row[0]}""")
                count = cur.fetchone()
                print(f'Компания: {row[1]}  /  Количество вакансий: {count[0]}')

        conn.close()

    @classmethod
    def get_all_vacancies(cls, database_name, params):
        """
        Получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию
        """
        conn = psycopg2.connect(dbname=database_name, **params)

        with conn.cursor() as cur:
            cur.execute("SELECT * FROM vacancies")
            rows = cur.fetchall()
            for row in rows:
                cur.execute(f"""select * from companies
                                where company_id = {row[3]}""")
                company = cur.fetchone()
                print(f"""Вакансия: {row[1]}  /  Ссылка: {row[2]} 
Компания: {company[1]}  /  Зарплата: от {row[4]} до {row[5]} рублей""")

        conn.close()

    @classmethod
    def get_avg_salary(cls, database_name, params):
        """
        Получает среднюю зарплату по вакансиям
        """
        conn = psycopg2.connect(dbname=database_name, **params)

        with conn.cursor() as cur:
            cur.execute("select AVG(salary_to) from vacancies")
            row = cur.fetchone()
            print(f'Средняя зарплата по вакансиям: {round(row[0])} рублей')

        conn.close()
    @classmethod
    def get_vacancies_with_higher_salary(cls, database_name, params):
        """
        Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям
        """
        conn = psycopg2.connect(dbname=database_name, **params)

        with conn.cursor() as cur:
            cur.execute("""select * from vacancies
where salary_to > (select AVG(salary_to) from vacancies)""")
            rows = cur.fetchall()
            for row in rows:
                print(f'''Вакансия: {row[1]}  /  Ссылка: {row[2]} 
Зарплата до {row[5]} рублей''')

    @classmethod
    def get_vacancies_with_keyword(cls, database_name, params):
        """
        Получает список всех вакансий,
        в названии которых содержатся переданные в метод слова
        """
        keyword = input('Введите ключевое слово (чувствительно к регистру!!!): ')
        conn = psycopg2.connect(dbname=database_name, **params)

        with conn.cursor() as cur:
            cur.execute(f"""select * from vacancies
where vacancy_name like '%{keyword}%'""")
            rows = cur.fetchall()
            if rows == []:
                print('По вашему запросу ничего не найдено!')
            else:
                for row in rows:
                    print(f'''Вакансия: {row[1]}  /  Ссылка: {row[2]} 
            Зарплата до {row[5]} рублей''')


    @classmethod
    def start_working(cls, database_name, params):
        print('Добро пожаловать! Выберите действие:')
        while True:
            answer = input("""0. Завершение работы
1. Получить список всех компаний и количество вакансий у каждой компании
2. Получить список всех вакансий с указанием названия компании,
названия вакансии и зарплаты и ссылки на вакансию
3. Получить среднюю зарплату по найденным вакансиям
4. Получить список всех вакансий, у которых зарплата выше средней по всем вакансиям
5. Получить список всех вакансий,
в названии которых содержатся переданные в метод слова
Ваш вариант: """)
            if answer == '0':
                print('Программа прекращает работу')
                break
            elif answer == '1':
                cls.get_companies_and_vacancies_count(database_name, params)
            elif answer == '2':
                cls.get_all_vacancies(database_name, params)
            elif answer == '3':
                cls.get_avg_salary(database_name, params)
            elif answer == '4':
                cls.get_vacancies_with_higher_salary(database_name, params)
            elif answer == '5':
                cls.get_vacancies_with_keyword(database_name, params)
            else:
                print('Некорректный ввод, программа прекращает работу')
                break

