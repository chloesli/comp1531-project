
from abc import ABC, abstractmethod

class Drink():
    def __init__(self, name, drink_type, amount):
        self._name = name
        self._drink_type = drink_type
        self._amount = amount

    def get_price(self):
        # if can then $$ if bottle then $$$
        if self._drink_type == "can": 
            return 2
        if self._drink_type == "bottle": 
            return 3
        if self._drink_type == "small": 
            return 2
        if self._drink_type == "medium":
            return 2.50
        if self._drink_type == "large":
            return 2.95
        
        return 0
 
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
    def drink_type(self):
        return self._drink_type
    
    @drink_type.setter
    def drink_type(self, drink_type):
        self._drink_type = drink_type

    @property
    def amount(self):
        return self._amount
    
    @amount.setter
    def amount(self, amount):
        self._amount = amount

    def __str__(self):
        n =  f'{self._name.title()}'

        if self._drink_type != None or self._drink_type != "":
            n += f' {self._drink_type.capitalize()}'

        return n
