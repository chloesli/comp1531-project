class Sundae():
    def __init__(self, flavour, size, amount):
        self._flavour = flavour
        self._size = size
        self._amount = amount
    
    def get_price(self):
        if self._size == "small":
            return 2.0
        if self._size == "medium":
            return 2.50
        if self._size == "large":
            return 3.0
        
        return 0
    
    @property
    def flavour(self):
        return self._flavour
    
    @property
    def amount(self):
        return self._amount
    
    def __str__(self):
        return f'{self._flavour} Sundae ({self._size})'
