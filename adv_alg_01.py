# Продвинутые алгоритмы (задание 01)
# Необходимо реализовать скрипт на Python в котором будет
# базовый класс и класс наследник от
# базового класса.

import requests
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
from typing import List, Dict


class BaseModel(ABC):
    """Базовый абстрактный класс для работы с веб-сайтами"""

    @abstractmethod
    def fetch_data(self, categories: List[str]) -> None:
        """Метод для получения данных с веб-сайта по указанным категориям"""
        pass

    @abstractmethod
    def to_dict(self) -> Dict:
        """Метод для преобразования данных в словарь"""
        pass


class WoysaClubParser(BaseModel):
    """Класс для парсинга данных с сайта woysa.club (реализован как синглтон)"""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(WoysaClubParser, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.data = {}
        self.base_url = "https://woysa.club"

    def fetch_data(self, categories: List[str]) -> None:
        """Получение данных с сайта woysa.club по указанным категориям"""

        for category in categories:
            try:
                url = f"{self.base_url}/{category}"
                response = requests.get(url)
                response.raise_for_status()

                soup = BeautifulSoup(response.text, 'html.parser')

                # Здесь можно добавить конкретную логику парсинга
                # Например, извлечение заголовков статей
                articles = []
                for article in soup.find_all('article'):
                    title = article.find('h2').text.strip() if article.find('h2') else 'No title'
                    link = article.find('a')['href'] if article.find('a') else '#'
                    articles.append({'title': title, 'link': link})

                self.data[category] = articles

            except requests.exceptions.RequestException as e:
                print(f"Ошибка при получении данных для категории {category}: {e}")
                self.data[category] = []

    def to_dict(self) -> Dict:
        """Преобразование полученных данных в словарь"""
        return self.data


# Пример использования
if __name__ == "__main__":
    # Создаем первый экземпляр
    parser1 = WoysaClubParser()
    parser1.fetch_data(['#rec580600206', '#rec582709478'])

    # Создаем второй экземпляр (должен быть тем же самым объектом)
    parser2 = WoysaClubParser()
    parser2.fetch_data(['#rec581311284'])

    # Проверка, что это один и тот же объект
    print(parser1 is parser2)  # Должно вывести True

    # Получаем данные в виде словаря
    data_dict = parser1.to_dict()
    print(data_dict)