import psycopg2 as psycopg2
import requests


def get_hh_ru_data(employers_ids):
    """Функция получения ответа от API"""

    data = []
    for employers_id in employers_ids:
        company = requests.get(f'https://api.hh.ru/employers/{employers_id}').json()
        vacancies = requests.get(f'https://api.hh.ru/vacancies?employer_id={employers_id}').json()
        data.append({
            'company': company,
            'vacancies': vacancies
        })
    return data


def create_database(database_name: str, params: dict):
    """Функция создания пустой базы данных"""

    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE IF EXISTS {database_name}")
    cur.execute(f"CREATE DATABASE {database_name}")

    conn.close()

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE companies (
                company_id SERIAL PRIMARY KEY,
                company_name VARCHAR(255) NOT NULL,
                city TEXT,
                site_url TEXT
            )
        """)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE vacancies (
                vacancy_id SERIAL PRIMARY KEY,
                vacancy_name VARCHAR(255) NOT NULL,
                vacancy_url TEXT,
                employer_id INT REFERENCES companies(company_id),
                salary_from INTEGER,
                salary_to INTEGER
            )
        """)

    conn.commit()
    conn.close()


def save_data_to_database(data, database_name, params):
    """Функция заполнения информацией базы данных"""

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        for company in data:
            company_data = company['company']
            cur.execute(
                """
                INSERT INTO companies (company_name, city, site_url)
                VALUES (%s, %s, %s)
                RETURNING company_id
                """,
                (company_data['name'], company_data['area']['name'], company_data['alternate_url'])
            )
            company_id = cur.fetchone()[0]
            vacancies_data = company['vacancies']['items']
            for vacancy in vacancies_data:
                if vacancy['salary'] is None:
                    salary_from = 0
                    salary_to = 0
                elif vacancy['salary']['from'] is None and vacancy['salary']['to']:
                    salary_from = vacancy['salary']['to']
                    salary_to = vacancy['salary']['to']
                elif vacancy['salary']['from'] and vacancy['salary']['to'] is None:
                    salary_from = vacancy['salary']['from']
                    salary_to = vacancy['salary']['from']
                else:
                    salary_from = vacancy['salary']['from']
                    salary_to = vacancy['salary']['to']
                cur.execute(
                    """
                    INSERT INTO vacancies (vacancy_name, vacancy_url, employer_id, salary_from, salary_to)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (vacancy['name'], vacancy['alternate_url'], company_id, salary_from, salary_to)
                )

    conn.commit()
    conn.close()



