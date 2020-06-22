class IdGenerator():
    def __init__(self, value = -1):
        self._id = value
    
    def next(self):
        self._id += 1
        return self._id

order_id = IdGenerator()

class Order():
    def __init__(self):
        self._order_id = order_id.next()
        self._status = False
        self._price = 0.0

        self._completed = False
        
        self._sides = []
        self._drinks = []
        self._mains = []
        self._sundaes = []

    @property
    def order_id(self):
        return self._order_id

    @property
    def completed(self):
        return self._completed
    
    @completed.setter
    def completed(self, completed):
        self._completed = completed

    @property
    def sides(self):
        return self._sides

    def add_side(self, side):
        self._sides.append(side)

    @property
    def drinks(self):
        return self._drinks

    def add_drink(self, drink):
        self._drinks.append(drink)

    @property
    def mains(self):
        return self._mains

    def add_main(self, main):
        self._mains.append(main)
    
    @property
    def sundaes(self):
        return self._sundaes
        
    def add_sundae(self, sundae):
        self._sundaes.append(sundae)

    def calculate_price(self):
        price = 0

        for side in self._sides:
            price += side.price

        for drink in self._drinks:
            price += drink.get_price()

        for main in self._mains:
            price += main.get_total_price()
        
        for sundae in self._sundaes:
            price += sundae.get_price()

        return price
    
    def displayOrder(self):
        for side in self._sides: 
            print(side)
        for drink in self._drinks:
            print(drink)
        for main in self._mains:
            print(main)
            print([str(x) for x in main._ingredients])
