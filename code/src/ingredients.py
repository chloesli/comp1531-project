from abc import ABC, abstractmethod

class Ingredient(ABC):
    def __init__(self, name, i_type, readable_name, amount=1, price=0):
        self._name = name
        self._type = i_type
        self._readable_name = readable_name
        self._amount = amount
        self._price = price           

    @property
    def inv_id(self):
        return self._inv_id
    
    @inv_id.setter
    def inv_id(self, id):
        self._inv_id = id
  
    @property
    def name(self):
        return self._name
    
    @property
    def readable_name(self):
        return self._readable_name
    
    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, amount):
        self._amount = amount

    @property
    def i_type(self):
        return self._type

    @property
    def price(self):
        return self._price
    
    def __str__(self):
        return f'{self._readable_name}'

    def __repr__(self):
        return f'<{self._type}: {self._name}, {self._amount}, {self._price}>'

