# Продвинутые алгоритмы (задание 01)
# Необходимо реализовать скрипт на Python в котором будет
# базовый класс и класс наследник от
# базового класса.

import requests
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
from typing import List, Dict

class BaseModel(ABC):

    @abstractmethod
    def fetch_data(self, categories: List[str]) -> None:

        pass

    @abstractmethod
    def to_dict(self) -> Dict:

        pass

class WoysaClubParser(BaseModel):

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

        for category in categories:
            try:
                url = f"{self.base_url}/{category}"
                response = requests.get(url)
                response.raise_for_status()

                soup = BeautifulSoup(response.text, 'html.parser')

            except requests.exceptions.RequestException as e:
                print(f"Ошибка при получении данных для категории {category}: {e}")
                self.data[category] = []

    def to_dict(self) -> Dict:

        return self.data

# Пример использования
if __name__ == "__main__":
    # Создаем первый экземпляр
    parser1 = WoysaClubParser()
    parser1.fetch_data(['#rec580600206', '#rec582709478'])

    # Создаем второй экземпляр
    parser2 = WoysaClubParser()
    parser2.fetch_data(['#rec581311284'])

    # Проверка, что это один и тот же объект
    print(parser1 is parser2)  # Должно вывести True

    # Получаем данные в виде словаря
    data_dict = parser1.to_dict()
    print(data_dict)