
class Player:
    def __init__(self,DB_ID,LOC,CO2_Budget,Fuel,Money,BoughtExtraCash,BoughtFuelTank):
        self.databaseID = DB_ID
        self.location = LOC
        self.CO2_Budget = CO2_Budget
        self.Fuel = Fuel
        self.Money = Money
        self.Fuel_Efficiency = 10
        # this part will remember if the player has taken up a quest. This is about to get real messy
        self.quest = [False, False]
        # Takes new location (IDENT) and updates it for object and for database
        self.BoughtFuelTank = BoughtFuelTank
        self.BoughtExtraCash = BoughtExtraCash
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

