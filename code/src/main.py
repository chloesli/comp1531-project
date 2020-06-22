from abc import ABC, abstractmethod
from src.ingredients import Ingredient

class Main(ABC):
    def __init__(self, m_type, ingredients):
        self._type = m_type

        self._ingredients = ingredients

    def get_total_price(self):
        price = 0

        for item in self._ingredients:
            price += item._price * item._amount

        return price

    @property
    def ingredients(self):
        return self._ingredients
            
    def __str__(self):
        return f'{self._type.capitalize()}'

