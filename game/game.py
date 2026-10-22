"""Модуль с интерфейсом и реализацией класса игры"""

from abc import ABC, abstractmethod
from dataclasses import replace
from typing import Any

from .clicker import AbstractClicker
from .exceptions import NotEnoughMoney
from .models import Food, Medicine
from .tamagochi import AbstractTamagochi

START_COINS = 0


class AbstractGame(ABC):
    """Интерфейс для логики игры"""

    @abstractmethod
    def __init__(
        self,
        tamagochi: AbstractTamagochi,
        clicker: AbstractClicker,
        all_food: list[Food],
        all_medicine: list[Medicine],
    ) -> None:
        """
        Абстрактный метод инициализации класса игры

        :param tamagochi: экземпляр тамагочи
        :param clicker: экземпляр кликера
        :param all_food: все доступные варианты еды
        :param all_medicine: все доступные варианты лекарств
        """
        raise NotImplementedError

    @abstractmethod
    def work(self) -> int:
        """
        Абстрактный метод для логики действия "работа"

        :return: количество заработанных монет
        """
        raise NotImplementedError

    @abstractmethod
    def buy_food(self) -> None:
        """Абстрактный метод для покупки еды"""
        raise NotImplementedError

    @abstractmethod
    def buy_medicine(self) -> None:
        """Абстрактный метод для покупки лекарства"""
        raise NotImplementedError

    @abstractmethod
    def feed_tamagochi(self) -> None:
        """Абстрактный метод для кормления тамагочи"""
        raise NotImplementedError

    @abstractmethod
    def heal_tamagochi(self) -> None:
        """Абстрактный метод для лечения тамагочи"""
        raise NotImplementedError

    @abstractmethod
    def rest_tamagochi(self) -> None:
        """Абстрактный метод для отдыха тамагочи"""
        raise NotImplementedError

    @abstractmethod
    def play_with_tamagochi(self) -> None:
        """Абстрактный метод для игры с тамагочи"""
        raise NotImplementedError

    @abstractmethod
    def get_status(self) -> dict[str, Any]:
        """
        Абстрактный метод для получения статуса игры

        :return: словарь со всеми характеристиками тамагочи и монетами
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def tamagochi(self) -> AbstractTamagochi:
        """
        Абстрактное свойство для доступа к тамагочи

        :return: экземпляр тамагочи
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def food(self) -> list[Food]:
        """
        Абстрактное свойство для доступа к сумке с едой

        :return: список с имеющимися (купленными) объектами еды
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def medicine(self) -> list[Medicine]:
        """
        Абстрактное свойство для доступа к сумке с лекарствами

        :return: список с имеющимися (купленными) объектами лекарств
        """
        raise NotImplementedError


class SimpleGame(AbstractGame):
    """Простая реализация игры"""

    def __init__(
        self,
        tamagochi: AbstractTamagochi,
        clicker: AbstractClicker,
        all_food: list[Food],
        all_medicine: list[Medicine],
    ) -> None:
        """
        Инициализация игры с тамагочи, кликером, едой и лекарствами

        :param tamagochi: экземпляр тамагочи
        :param clicker: экземпляр кликера
        :param all_food: каталог еды, доступной для покупки
        :param all_medicine: каталог лекарств, доступных для покупки
        """
        self._tamagochi = tamagochi
        self._clicker = clicker
        self._all_food = all_food
        self._all_medicine = all_medicine
        self._coins = START_COINS
        self._food_bag: list[Food] = []
        self._medicine_bag: list[Medicine] = []

    def work(self) -> int:
        """
        Метод для логики действия "работа"

        :return: количество заработанных монет
        """
        self._clicker.click()
        income = self._clicker.income_per_click
        self._coins += income
        self._tamagochi.update()
        return income

    def buy_food(self) -> None:
        """
        Метод для покупки еды

        :raises ValueError: если выбран неверный номер
        :raises NotEnoughMoney: если не хватает монет
        """
        item = self._choose_from(self._all_food)
        self._pay(item.price)
        self._food_bag.append(item)

    def buy_medicine(self) -> None:
        """
        Метод для покупки лекарства

        :raises ValueError: если выбран неверный номер
        :raises NotEnoughMoney: если не хватает монет
        """
        item = self._choose_from(self._all_medicine)
        self._pay(item.price)
        self._medicine_bag.append(replace(item))

    def get_status(self) -> dict[str, Any]:
        """
        Метод для получения статуса тамагочи и монет

        :return: словарь с характеристиками тамагочи и ключом coins
        """
        return {**self._tamagochi.status, "coins": self._coins}

    @property
    def tamagochi(self) -> AbstractTamagochi:
        """
        Свойство для доступа к тамагочи (только чтение)

        :return: экземпляр тамагочи
        """
        return self._tamagochi

    @property
    def food(self) -> list[Food]:
        """
        Свойство для доступа к сумке с едой

        :return: копия списка купленной еды
        """
        return list(self._food_bag)

    @property
    def medicine(self) -> list[Medicine]:
        """
        Свойство для доступа к сумке с лекарствами

        :return: копия списка купленных лекарств
        """
        return list(self._medicine_bag)

    def _choose_from(self, catalog: list[Any]) -> Any:
        """
        Показывает каталог и возвращает выбранный товар

        :param catalog: список товаров для выбора
        :return: выбранный товар
        :raises ValueError: если введён не номер или номера нет в списке
        """
        for number, item in enumerate(catalog, start=1):
            print(f"{number}. {item}")
        choice = int(input("Введите номер: ")) - 1
        if not 0 <= choice < len(catalog):
            raise ValueError("Нет товара с таким номером")
        return catalog[choice]

    def _pay(self, price: int) -> None:
        """
        Списывает монеты за покупку

        :param price: цена покупки
        :raises NotEnoughMoney: если монет меньше цены
        """
        if price > self._coins:
            raise NotEnoughMoney("Не хватает монет")
        self._coins -= price

    def feed_tamagochi(self) -> None:
        """
        Метод для кормления тамагочи

        :raises ValueError: если сумка пуста или выбран неверный номер
        """
        if not self._food_bag:
            raise ValueError("Сумка с едой пуста")
        food = self._choose_from(self._food_bag)
        self._tamagochi.feed(food)
        self._food_bag.remove(food)
        self._tamagochi.update()

    def heal_tamagochi(self) -> None:
        """
        Метод для лечения тамагочи

        :raises ValueError: если сумка пуста или выбран неверный номер
        """
        if not self._medicine_bag:
            raise ValueError("Сумка с лекарствами пуста")
        medicine = self._choose_from(self._medicine_bag)
        self._tamagochi.heal(medicine)
        if medicine.is_empty():
            self._medicine_bag.remove(medicine)
        self._tamagochi.update()

    def rest_tamagochi(self) -> None:
        """Метод для отдыха тамагочи"""
        self._tamagochi.rest()
        self._tamagochi.update()

    def play_with_tamagochi(self) -> None:
        """Метод для игры с тамагочи"""
        self._tamagochi.play()
        self._tamagochi.update()
