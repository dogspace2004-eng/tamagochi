"""Модуль с интерфейсом и реализациями класса тамагочи"""

from abc import ABC, abstractmethod

from .models import Food, Medicine

# Констатнты для максимальных состояний тамагочи
HUNGER_MAX = 100
HP_MAX = 100
ENERGY_MAX = 100
# Константы для восстановления состояний
REST_ENERGY_RESTORE = 20
REST_HUNGER_RESTORE = 5
# Константы для уменьшения состояний
PLAY_ENERGY_DECREASE = 10
PLAY_HUNGER_DECREASE = 5
# Константы для минимальных состояний
HUNGER_MIN = 0
HP_MIN = 0
ENERGY_MIN = 0
# Константы для обновления состояний
HUNGER_PER_TICK = 5
ENERGY_PER_TICK = 5
# Константы для штрафов при болезни и голоде
SICK_HP_PENALTY = 5
STARVING_HP_PENALTY = 10


class AbstractTamagochi(ABC):
    """Интерфейс логики тамагочи"""

    @abstractmethod
    def feed(self, food: Food) -> None:
        """
        Абстрактный метод для кормления тамагочи

        :param food: объект еды для кормления
        """
        raise NotImplementedError

    @abstractmethod
    def play(self) -> None:
        """Абстрактный метод для игры с тамагочи"""
        raise NotImplementedError

    @abstractmethod
    def rest(self) -> None:
        """Абстрактный метод для отдыха тамагочи"""
        raise NotImplementedError

    @abstractmethod
    def heal(self, medicine: Medicine) -> None:
        """
        Абстрактный метод для лечения тамагочи

        :param medicine: лекарство для лечения
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def status(self) -> dict[str, int]:
        """
        Абстрактное свойство для доступа ко всем состояниям тамагочи

        :return: словарь со всеми состояниями тамагочи
        """
        raise NotImplementedError

    @abstractmethod
    def is_alive(self) -> bool:
        """
        Абстрактный метод для проверки жив ли тамагочи

        :return: True если жив, иначе False
        """
        raise NotImplementedError

    @abstractmethod
    def is_sick(self) -> bool:
        """
        Абстрактный метод для проверки, не заболел ли тамагочи

        :return: True если тамагочи болеет, иначе False
        """
        raise NotImplementedError

    @abstractmethod
    def update(self) -> None:
        """
        Абстрактный метод для обновления состояний тамагочи.
        Должен использоваться после каждого взаимодействия с тамагочи
        """
        raise NotImplementedError


class SimpleTamagochi(AbstractTamagochi):
    """Простая реализация тамагочи"""

    def __init__(self) -> None:
        """Инициализация тамагочи с максимальными состояниями"""
        self._hunger = 0
        self._hp = HP_MAX
        self._energy = ENERGY_MAX

    def feed(self, food: Food) -> None:
        """
        Метод для кормления тамагочи

        :param food: объект еды для кормления
        """
        self._hunger = max(self._hunger - food.satiety, HUNGER_MIN)

    def play(self) -> None:
        """Метод для игры с тамагочи"""
        self._energy = max(self._energy - PLAY_ENERGY_DECREASE, ENERGY_MIN)
        self._hunger = min(self._hunger + PLAY_HUNGER_DECREASE, HUNGER_MAX)

    def rest(self) -> None:
        """Метод для отдыха тамагочи"""
        if self.is_sick():
            energy_restore = REST_ENERGY_RESTORE // 2
        else:
            energy_restore = REST_ENERGY_RESTORE
        self._energy = min(self._energy + energy_restore, ENERGY_MAX)
        self._hunger = min(self._hunger + REST_HUNGER_RESTORE, HUNGER_MAX)

    def heal(self, medicine: Medicine) -> None:
        """
        Метод для лечения тамагочи

        :param medicine: лекарство для лечения
        """
        if not medicine.is_empty():
            self._hp = min(self._hp + medicine.heal_hp, HP_MAX)
            medicine.uses += 1

    @property
    def status(self) -> dict[str, int]:
        """Получение текущего состояния тамагочи в виде словаря"""
        return {
            "hunger": self._hunger,
            "hp": self._hp,
            "energy": self._energy
        }

    def is_alive(self) -> bool:
        """Тамагочи жив, если его здоровье больше нуля"""
        return self._hp > 0

    def is_sick(self) -> bool:
        """
        Тамагочи болеет, если его здоровье меньше половины максимального
        или голод больше половины максимального
        :return: True если тамагочи болеет, иначе False
        """
        return self._hp < HP_MAX // 2 or self._hunger > HUNGER_MAX // 2

    def update(self) -> None:
        """
        Обновляет состояние питомца за один ход.

        Голод растёт, энергия падает. Если питомец болен, он теряет
        здоровье. Если голод на максимуме, здоровье падает сильнее.
        """
        self._hunger = min(self._hunger + HUNGER_PER_TICK, HUNGER_MAX)
        self._energy = max(self._energy - ENERGY_PER_TICK, ENERGY_MIN)
        if self.is_sick():
            self._hp = max(self._hp - SICK_HP_PENALTY, HP_MIN)
        if self._hunger == HUNGER_MAX:
            self._hp = max(self._hp - STARVING_HP_PENALTY, HP_MIN)
