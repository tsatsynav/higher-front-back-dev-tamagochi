"""Модуль с интерфейсом и реализацией кликера."""

import random
from abc import ABC, abstractmethod


class AbstractClicker(ABC):
    """Интерфейс для кликера."""

    @abstractmethod
    def __init__(self) -> None:
        """Абстрактный метод инициализации."""
        raise NotImplementedError

    @abstractmethod
    def click(self) -> None:
        """Абстрактный метод клика для накапливания монет."""
        raise NotImplementedError

    @property
    @abstractmethod
    def income_per_click(self) -> int:
        """Абстрактное свойство: доход за один клик."""
        raise NotImplementedError


class SimpleRandomClicker(AbstractClicker):
    """Кликер со случайным доходом в заданном диапазоне."""

    def __init__(
        self,
        min_income: int = 5,
        max_income: int = 15,
    ) -> None:
        """Инициализирует кликер.

        :param min_income: минимальный доход за клик.
        :param max_income: максимальный доход за клик.
        """
        if min_income > max_income:
            raise ValueError(
                'min_income не может быть больше max_income'
            )
        self._min_income = min_income
        self._max_income = max_income
        self._current_income = min_income

    def click(self) -> None:
        """Совершает клик: выбирает новый случайный доход."""
        self._current_income = random.randint(
            self._min_income, self._max_income
        )

    @property
    def income_per_click(self) -> int:
        """Возвращает доход за последний клик."""
        return self._current_income
