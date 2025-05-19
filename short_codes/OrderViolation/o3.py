import random
import time

class restaurant:
    def __init__(self):
        self.OrderList = []
        self.Cooking = []
        self.finish = []
    
    def OrderRecieved(self, menu):
        OrderNumber = len(self.OrderList) + 1
        self.OrderList.append((OrderNumber, menu))
        print(f"[OrderRecieved] OrderNumber {OrderNumber}: {menu}")
        return OrderNumber
    
    def startCooking(self):
        if not self.OrderList:
            return False
        
        choice_index = random.randint(0, len(self.OrderList)-1)
        OrderNumber, menu = self.OrderList.pop(choice_index)
        
        self.Cooking.append((OrderNumber, menu))
        print(f"[startCooking] OrderNumber {OrderNumber}: {menu} - there is possibility of Order Violation!!")
        return True
    
    def cookingfinish(self):
        if not self.Cooking:
            return False
        
        choice_index = random.randint(0, len(self.Cooking)-1)
        OrderNumber, menu = self.Cooking.pop(choice_index)
        
        self.finish.append((OrderNumber, menu))
        print(f"[cookingfinish] OrderNumber {OrderNumber}: {menu} - here is possibility of Order Violation!!")
        return True


def simulation():
    restaurant = restaurant()
    menuList = ["Bibimbap", "Kimchi Jjigae", "Bulgogi", "Doenjang Jjigae", "Tteokbokki"]
    
    for menu in menuList:
        restaurant.OrderRecieved(menu)
    
    while restaurant.OrderList or restaurant.Cooking:
        if restaurant.OrderList and random.random() < 0.7:
            restaurant.startCooking()
        if restaurant.Cooking and random.random() < 0.5:
            restaurant.cookingfinish()
        time.sleep(0.5)
    
    print("\nfinal finished order:")
    for Number, menu in restaurant.finish:
        print(f"OrderNumber {Number}: {menu}")

simulation()
