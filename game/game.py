"""Модуль с интерфейсом и реализацией класса игры."""

from abc import ABC, abstractmethod
from typing import Any

from .clicker import AbstractClicker
from .models import Food, Medicine
from .tamagochi import AbstractTamagochi


class AbstractGame(ABC):
    """Интерфейс для логики игры."""

    @abstractmethod
    def __init__(
        self,
        tamagochi: AbstractTamagochi,
        clicker: AbstractClicker,
        all_food: list[Food],
        all_medicine: list[Medicine],
    ) -> None:
        """Инициализация игры."""
        raise NotImplementedError

    @abstractmethod
    def work(self) -> int:
        """Логика действия «пойти на работу»."""
        raise NotImplementedError

    @abstractmethod
    def buy_food(self) -> None:
        """Логика покупки еды."""
        raise NotImplementedError

    @abstractmethod
    def buy_medicine(self) -> None:
        """Логика покупки лекарства."""
        raise NotImplementedError

    @abstractmethod
    def feed_tamagochi(self) -> None:
        """Логика кормления питомца."""
        raise NotImplementedError

    @abstractmethod
    def heal_tamagochi(self) -> None:
        """Логика лечения питомца."""
        raise NotImplementedError

    @abstractmethod
    def rest_tamagochi(self) -> None:
        """Логика отдыха питомца."""
        raise NotImplementedError

    @abstractmethod
    def play_with_tamagochi(self) -> None:
        """Логика игры с питомцем."""
        raise NotImplementedError

    @abstractmethod
    def get_status(self) -> dict[str, Any]:
        """Получение полного статуса игры."""
        raise NotImplementedError

    @property
    @abstractmethod
    def food(self) -> list[Food]:
        """Сумка с едой."""
        raise NotImplementedError

    @property
    @abstractmethod
    def medicine(self) -> list[Medicine]:
        """Аптечка."""
        raise NotImplementedError


class SimpleGame(AbstractGame):
    """Простая реализация игры."""

    def __init__(
        self,
        tamagochi: AbstractTamagochi,
        clicker: AbstractClicker,
        all_food: list[Food],
        all_medicine: list[Medicine],
    ) -> None:
        """Инициализирует игру.

        :param tamagochi: экземпляр питомца.
        :param clicker: экземпляр кликера.
        :param all_food: варианты еды в магазине.
        :param all_medicine: варианты лекарств в магазине.
        """
        self.tamagochi = tamagochi
        self._clicker = clicker
        self._all_food = list(all_food)
        self._all_medicine = list(all_medicine)
        self._food_inventory: list[Food] = []
        self._medicine_inventory: list[Medicine] = []
        self._coins = 0

    def work(self) -> int:
        """Работа: клик и начисление монет.

        :return: сколько монет заработано.
        """
        self._clicker.click()
        income = self._clicker.income_per_click
        self._coins += income
        return income

    def buy_food(self) -> None:
        """Покупка еды из доступного списка."""
        while True:
            print('Доступная еда:')
            for i, food in enumerate(self._all_food, start=1):
                print(f'  {i}. {food}')
            print('  0. Выход')
            try:
                choice = int(input('Выберите еду: '))
            except (ValueError, EOFError):
                print('Неверная команда')
                continue
            if choice == 0:
                return
            if not 1 <= choice <= len(self._all_food):
                print('Неверный номер')
                continue
            food = self._all_food[choice - 1]
            if self._coins >= food.price:
                self._coins -= food.price
                self._food_inventory.append(food)
                print(f'Куплено: {food.name}')
            else:
                print('Не хватает монет!')

    def buy_medicine(self) -> None:
        """Покупка лекарства из доступного списка."""
        while True:
            print('Доступные лекарства:')
            for i, med in enumerate(self._all_medicine, start=1):
                print(f'  {i}. {med}')
            print('  0. Выход')
            try:
                choice = int(input('Выберите лекарство: '))
            except (ValueError, EOFError):
                print('Неверная команда')
                continue
            if choice == 0:
                return
            if not 1 <= choice <= len(self._all_medicine):
                print('Неверный номер')
                continue
            med = self._all_medicine[choice - 1]
            if self._coins >= med.price:
                self._coins -= med.price
                self._medicine_inventory.append(med)
                print(f'Куплено: {med.name}')
            else:
                print('Не хватает монет!')

    def feed_tamagochi(self) -> None:
        """Кормит питомца выбранной едой."""
        if not self._food_inventory:
            print('В сумке нет еды!')
            return
        print('Сумка с едой:')
        for i, food in enumerate(self._food_inventory, start=1):
            print(f'  {i}. {food}')
        try:
            choice = int(input('Выберите еду: '))
        except (ValueError, EOFError):
            print('Неверная команда')
            return
        if not 1 <= choice <= len(self._food_inventory):
            print('Неверный номер')
            return
        food = self._food_inventory.pop(choice - 1)
        self.tamagochi.feed(food)
        print(f'Питомец съел: {food.name}')

    def heal_tamagochi(self) -> None:
        """Лечит питомца выбранным лекарством."""
        if not self._medicine_inventory:
            print('В аптечке нет лекарств!')
            return
        print('Аптечка:')
        for i, med in enumerate(self._medicine_inventory, start=1):
            print(f'  {i}. {med}')
        try:
            choice = int(input('Выберите лекарство: '))
        except (ValueError, EOFError):
            print('Неверная команда')
            return
        if not 1 <= choice <= len(self._medicine_inventory):
            print('Неверный номер')
            return
        med = self._medicine_inventory[choice - 1]
        if med.is_empty():
            self._medicine_inventory.pop(choice - 1)
            print('Лекарство закончилось и было выброшено')
            return
        self.tamagochi.heal(med)
        print(f'Использовано: {med.name}')
        if med.is_empty():
            self._medicine_inventory.pop(choice - 1)

    def rest_tamagochi(self) -> None:
        """Даёт питомцу отдохнуть."""
        self.tamagochi.rest()

    def play_with_tamagochi(self) -> None:
        """Играет с питомцем."""
        self.tamagochi.play()

    def get_status(self) -> dict[str, Any]:
        """Возвращает статус питомца вместе с монетами."""
        result = dict(self.tamagochi.status)
        result['coins'] = self._coins
        return result

    @property
    def food(self) -> list[Food]:
        """Сумка с едой."""
        return self._food_inventory

    @property
    def medicine(self) -> list[Medicine]:
        """Аптечка с лекарствами."""
        return self._medicine_inventory
