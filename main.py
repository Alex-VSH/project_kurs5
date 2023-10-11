from config import config
from utils import get_hh_ru_data, create_database, save_data_to_database
from DBManager import DBManager


def main():
    employers_ids = [
        '2120',         # Азбука вкуса
        '193400',       # Автоваз
        '3802070',      # Haier
        '9004369',      # Завод металлоконструкций
        '15478',        # VK
        '27879',        # Теремок
        '9498112',      # Яндекс крауд
        '1919447',      # ООО Мегаперфюме
        '3772',         # ООО Алианта Групп
        '7969'          # ООО Мелитэк
    ]
    params = config()
    database_name = 'job_database'
    print('Загружаем данные, пожалуйста, подождите...')
    data = get_hh_ru_data(employers_ids)                    # Загрузка инфы с hh.ru
    create_database(database_name, params)                  # Создание базы данных
    save_data_to_database(data, database_name, params)      # Сохранение инфы в базу данных

    DBManager.start_working(database_name, params)          # Метод взаимодействия с пользователем


if __name__ == '__main__':
    main()
