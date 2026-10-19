"""Модуль с интерфейсом и реализацией кликера"""

from abc import ABC, abstractmethod
from random import randint


class AbstractClicker(ABC):
    """Интерфейс для кликера"""

    @abstractmethod
    def __init__(self) -> None:
        """Абстрактный метод инициализации"""
        raise NotImplementedError

    @abstractmethod
    def click(self) -> None:
        """Абстрактный метод клика для накапливания монет"""
        raise NotImplementedError

    @property
    @abstractmethod
    def income_per_click(self) -> int:
        """Абстрактное свойство для доступа к количеству монет за клик"""
        raise NotImplementedError


class SimpleRandomClicker(AbstractClicker):
    """Простой кликер с случайным доходом за клик."""

    def __init__(self, min_income: int, max_income: int) -> None:
        """
        Инициализация кликера с минимальным и максимальным доходом за клик

        :param min_income: минимальный доход за клик
        :param max_income: максимальный доход за клик
        :raises ValueError: если параметры некорректны
        """
        if min_income < 0 or max_income < 0:
            raise ValueError("Доход за клик не может быть отрицательным")
        if min_income > max_income:
            raise ValueError(
                "Минимальный доход за клик не может быть больше максимального"
            )
        self._min_income = min_income
        self._max_income = max_income
        self._income_per_click = min_income

    def click(self) -> None:
        """
        Генерирует случайное количество монет
        """
        self._income_per_click = randint(self._min_income, self._max_income)

    @property
    def income_per_click(self) -> int:
        """
        Свойство для доступа к количеству монет за клик
        :return: Количество монет за клик
        """
        return self._income_per_click
