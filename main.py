class Item:
    
    def __init__(self, name: str, price=0, quantity=0):
        
        assert price>=0, f"Price {price} is not greater than zero!"
        assert quantity>=0, f"Quanity {quantity} is not greater than zero!"
        
        self.name = name
        self.price = price
        self.quantity = quantity
        
    
    # outside the classes are called functions, inside classes are methods
    def calculate_total_price(self): # default argument taken by the class the method itself
        return self.price * self.quantity
        

item1 = Item("Phone", 100, 5)

item2 = Item("Brush", 1000, 3)
print(item2.calculate_total_price())

print(type(item1))
print(type(item1.name))
print(type(item1.price))
print(type(item1.quantity))