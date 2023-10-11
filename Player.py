
class Player:
    databaseID = 0
    location = "Placeholder"
    CO2_Budget = 10000
    Fuel = 100
    Money = 1000
    Fuel_Efficiency = 10
    #this part will remember if the player has taken up a quest. This is about to get real messy
    quest = [False,False]
    # Takes new location (IDENT) and updates it for object and for database
    BoughtFuelTank = False
    BoughtExtraCash = False
    def update_location(self, new_location, cursor):
        self.location = new_location
        cursor.execute(f"update game set location = '{new_location}' where id = '{self.databaseID}'")


    # Updates the fuel for object and db
    def update_fuel(self, new_fuel, cursor):
        self.Fuel = new_fuel
        cursor.execute(f"update game set fuel = {new_fuel} where id = '{self.databaseID}'")


    # updates the money for object and db
    def update_money(self, new_money, cursor):
        self.Money = new_money
        cursor.execute(f"update game set money = {new_money} where id = '{self.databaseID}'")

