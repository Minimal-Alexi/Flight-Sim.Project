from Database import getairport,getcoordinates,db_query,get_country_from_ident
import json
class Player:
    def __init__(self,database_id,location,username,CO2_Budget,Fuel,Money,Fuel_Efficiency,BoughtExtraCash,BoughtFuelTank,quests):
        self.databaseID = database_id
        self.username = username
        self.location = location
        self.CO2_Budget = CO2_Budget
        self.Fuel = Fuel
        self.Money = Money
        self.Fuel_Efficiency = Fuel_Efficiency
        # this part will remember if the player has taken up a quest. It is a simple list which contains two items, they can be either:
        #a) False
        #b) [reward_for_quest,number_of_airports_to_go_to,goal_tracker,country_where_quest_was_picked_up]
        #The first item represents the local quests, the second item represents the international quests.~Min/Alex
        self.Quest = quests
        self.BoughtFuelTank = bool(BoughtFuelTank)
        self.BoughtExtraCash = bool(BoughtExtraCash)

    # Takes new location (IDENT) and updates it for object and for database.~Ashifa
    def update_location(self, new_location):
        self.location = new_location
        db_query(f"update game set location = '{new_location}' where id = '{self.databaseID}'")
    # Updates the fuel for object and db.~Ashifa
    def update_fuel(self, new_fuel):
        self.Fuel = new_fuel
        db_query(f"update game set fuel = {new_fuel} where id = '{self.databaseID}'")
    # updates the money for object and db.~Ashifa
    def update_money(self, new_money):
        self.Money = new_money
        db_query(f"update game set money = {new_money} where id = '{self.databaseID}'")

    def update_all(self):
        Quest = json.dumps(self.Quest)
        db_query(f"update game set MONEY = {self.Money},"
                 f"CO2_BUDGET = {self.CO2_Budget},"
                 f"LOCATION = '{self.location}',"
                 f"FUEL = {self.Fuel},"
                 f"FUEL_EFFICIENCY = {self.Fuel_Efficiency},"
                 f"QUEST = '{Quest}',"
                 f"FUELTANK = {int(self.BoughtFuelTank)},"
                 f"CARGOCAPACITY = {int(self.BoughtExtraCash)} "
                 f"where id = '{self.databaseID}'")
    def Check_Quest(self,new_location):
        country = get_country_from_ident(new_location)
        if self.Quest[0] != False:
            if country == self.Quest[0][3] and self.Quest[0] != False:
                if self.Quest[0][2] < self.Quest[0][1]:
                    self.Quest[0][2]+=1
                if self.Quest[0][1] == self.Quest[0][2]:
                    self.update_money(self.Quest[0][0])
                    self.Quest[0] = False
        if self.Quest[1] != False:
            if country != self.Quest[1][3] and self.Quest[1] != False:
                if self.Quest[1][2] < self.Quest[1][1]:
                    self.Quest[1][2] += 1
                if self.Quest[1][1] == self.Quest[1][2]:
                    self.update_money(self.Quest[1][0])
                    self.Quest[1] = False

    def drive_player(self,new_location,distance):
        self.update_fuel(self.Fuel-distance/self.Fuel_Efficiency)
        self.location = new_location
        if self.BoughtFuelTank == True and self.Fuel >= 250 and self.Fuel <= 350:
            self.update_fuel(self.Fuel - 250)
        elif self.BoughtFuelTank == True:
            self.update_fuel(self.Fuel - self.Fuel)
        self.BoughtFuelTank = False
        print(f"User {self.databaseID} travelled to airport {getairport(self.location)} ({distance})")
        self.Check_Quest(new_location)
        self.update_all()

    def get_Player_data(self):
        print(f"User database ID is: {self.databaseID}")
        print(f"User username is: {self.username}")
        print(f"User location is: {self.location}")
        print(f"User CO2_Budget is: {self.CO2_Budget}")
        print(f"User Fuel is: {self.Fuel}")
        print(f"User Money is: {self.Money}")
        print(f"User Fuel_Efficiency is: {self.Fuel_Efficiency}")
        print(f"User quest is: {self.Quest}")
        print(f"User BoughtFuelTank is: {self.BoughtFuelTank}")
        print(f"User BoughtExtraCash is: {self.BoughtExtraCash}")

    #I could probably make smaller batches of JSON data to be sent, but right now I am on a crunch. So let's just have everything ~Min/Alex.
    def get_JSON_data(self):
        response = {
            "databaseID":self.databaseID,
            "username":self.username,
            "location_name":getairport(self.location),
            "location_icao":self.location,
            "location_coords":getcoordinates(self.location),
            "CO2_Budget":self.CO2_Budget,
            "Fuel":self.Fuel,
            "Money":self.Money,
            "Fuel_Efficiency":self.Fuel_Efficiency,
            "Quest":self.Quest,
            "BoughtFuelTank":self.BoughtFuelTank,
            "BoughtExtraCash":self.BoughtExtraCash
        }
        return response