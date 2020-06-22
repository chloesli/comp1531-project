from abc import ABC, abstractmethod

class Side(ABC):
    def __init__(self, name):
        self._name = name

    @property
    def id(self):
        return self._id

    @abstractmethod
    def amount(self):
        pass
    
    @abstractmethod
    def price(self):
        pass

    @property
    def name(self):
        return self._name

    def __str__(self):
        return f'{self._name}: {self._amount}'

class Fries(Side):
    def __init__(self, size=None, amount=None):
        super().__init__("fries")

        self._size = size

        if size == "small":
            self._amount = 250

        if size == "medium":
            self._amount = 400

        if size == "large":
            self._amount = 640

        if amount != None:
            self._amount = amount
    
    @property
    def size(self):
        return self._size
    
    @property
    def name(self):
        return self._name
    
    @property
    def price(self):
        return self._price
    
    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, amount):
        self._amount = amount

    @property
    def price(self):
        if self._size == "small":
            return 2
        if self._size == "medium":
            return 3
        if self._size == "large":
            return 3.50
            
        return 0

    def __str__(self):
        n = 'Fries'

        if self._size != None and self._size != "":
            n += f' ({self._size.capitalize()})'

        return n
        
class Nuggets(Side):

    def __init__(self, amount):
        super().__init__("nuggets")

        self._amount = amount
    
    @property
    def amount(self):
        return self._amount
    
    @amount.setter
    def amount(self, amount):
        self._amount = amount

    @property
    def price(self):
        if self._amount == 3:
            return 3
        if self._amount == 6:
            return 4.50
        
        return 0
        
    
    def __str__(self):
        n = 'Nuggets' 

        if self._amount != None and self.price != 0:
            n += f' ({self._amount})'

        return n


