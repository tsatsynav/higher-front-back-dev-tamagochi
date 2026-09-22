"""Модуль с интерфейсом и реализацией класса тамагочи."""

import random
from abc import ABC, abstractmethod

from .exceptions import TamagochiIsGone
from .models import Food, Medicine


class AbstractTamagochi(ABC):
    """Интерфейс логики тамагочи."""

    @abstractmethod
    def feed(self, food: Food) -> None:
        """Накормить питомца."""
        raise NotImplementedError

    @abstractmethod
    def play(self) -> None:
        """Поиграть с питомцем."""
        raise NotImplementedError

    @abstractmethod
    def rest(self) -> None:
        """Дать питомцу отдохнуть."""
        raise NotImplementedError

    @abstractmethod
    def heal(self, medicine: Medicine) -> None:
        """Вылечить питомца."""
        raise NotImplementedError

    @property
    @abstractmethod
    def status(self) -> dict[str, int]:
        """Словарь со всеми показателями питомца."""
        raise NotImplementedError

    @abstractmethod
    def is_alive(self) -> bool:
        """True, если питомец жив."""
        raise NotImplementedError

    @abstractmethod
    def is_sick(self) -> bool:
        """True, если питомец болеет."""
        raise NotImplementedError

    @abstractmethod
    def update(self) -> None:
        """Обновить состояние питомца (тик времени)."""
        raise NotImplementedError


class SimpleTamagochi(AbstractTamagochi):
    """Простая реализация питомца."""

    MAX_STAT: int = 100
    HUNGER_MIN: int = 3
    HUNGER_MAX: int = 8
    ENERGY_MIN: int = 2
    ENERGY_MAX: int = 5
    SICK_HUNGER: int = 70
    SICK_ENERGY: int = 20
    SICK_CHANCE: float = 0.3

    def __init__(self, name: str = 'Тамагочи') -> None:
        """Создаёт питомца с полными ресурсами.

        :param name: имя питомца.
        """
        self._name = name
        self._hunger = 0
        self._hp = self.MAX_STAT
        self._energy = self.MAX_STAT
        self._is_sick = False

    @property
    def name(self) -> str:
        """Имя питомца."""
        return self._name

    @property
    def status(self) -> dict[str, int]:
        """Текущие показатели питомца."""
        return {
            'hunger': self._hunger,
            'hp': self._hp,
            'energy': self._energy,
        }

    def is_alive(self) -> bool:
        """Проверяет, жив ли питомец."""
        return self._hp > 0

    def is_sick(self) -> bool:
        """Проверяет, болен ли питомец."""
        return self._is_sick

    def feed(self, food: Food) -> None:
        """Кормит питомца.

        :param food: объект еды.
        """
        self._hunger = max(0, self._hunger - food.satiety)
        self._energy = max(0, self._energy - 5)

    def play(self) -> None:
        """Играет с питомцем."""
        self._hunger = min(self.MAX_STAT, self._hunger + 15)
        self._energy = max(0, self._energy - 10)
        self._hp = max(0, self._hp - 3)

    def rest(self) -> None:
        """Даёт питомцу отдохнуть.

        Больной питомец восстанавливает меньше энергии.
        """
        gain = 10 if self._is_sick else 20
        self._energy = min(self.MAX_STAT, self._energy + gain)

    def heal(self, medicine: Medicine) -> None:
        """Лечит питомца.

        :param medicine: объект лекарства.
        :raises ValueError: если лекарство уже закончилось.
        """
        if medicine.is_empty():
            raise ValueError('Лекарство закончилось')
        self._hp = min(self.MAX_STAT, self._hp + medicine.heal_hp)
        medicine.uses += 1
        if self._hp > self.MAX_STAT // 2:
            self._is_sick = False

    def update(self) -> None:
        """Обновляет состояние питомца.

        :raises TamagochiIsGone: если HP упало до нуля.
        """
        self._hunger += random.randint(
            self.HUNGER_MIN, self.HUNGER_MAX
        )
        self._energy -= random.randint(
            self.ENERGY_MIN, self.ENERGY_MAX
        )

        if self._hunger >= self.MAX_STAT:
            self._hunger = self.MAX_STAT
            self._hp -= 8

        if self._energy <= 0:
            self._energy = 0
            self._hp -= 5

        if self._is_sick:
            self._hp -= 2

        if not self._is_sick:
            if self._hunger > self.SICK_HUNGER:
                if random.random() < self.SICK_CHANCE:
                    self._is_sick = True
            elif self._energy < self.SICK_ENERGY:
                if random.random() < self.SICK_CHANCE:
                    self._is_sick = True

        if self._hp <= 0:
            self._hp = 0
            raise TamagochiIsGone()
