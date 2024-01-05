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

import re

def is_base62(s):
    # Define the base62 character set
    base62_chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    
    # Check if the string contains only valid base62 characters
    return bool(re.match(f'^[{base62_chars}]+$', s))

# Example usage:
test_string = "6rqhFgbbKwnb9MLmUQDhG6"
result = is_base62(test_string)

if result:
    print(f"{test_string} is a valid base62 string.")
else:
    print(f"{test_string} is not a valid base62 string.")
