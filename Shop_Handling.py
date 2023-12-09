
def shop(user, ItemID):
    refuel = 100 - user.Fuel
    items = {
        1: {"name": "+5km/l Fuel Efficiency", "money_price": 1000, "CO2_price": 100},
        2: {"name": "Refueling Services", "money_price": refuel*10, "CO2_price": refuel*10+500},
        3: {"name":"Environmental-Friendly Refueling Services", "money_price": refuel * 10 + 500,"CO2_price" : refuel * 10},
        4:{"name":"One-Time Extra Cargo capacity","money_price": 200, "CO2_price": 250},
        5:{"name":"One-Time Fuel Drop Tanks","money_price": 350, "CO2_price": 1000 },
    }

    # check which item the user purchases
    selected_item = items[ItemID]

    # check if user has money
    if user.Money < selected_item["money_price"]:
        needed_money = selected_item["money_price"]-user.Money
        response = {"status": f"Error", "message": "You don't have enough money. You need " + str(needed_money) + " euros"}
        return response

    # adjust player variables based on item
    user.Money -= selected_item["money_price"]
    user.CO2_Budget -= selected_item["CO2_price"]

    # item's effect on player variables
    if selected_item["name"] == "+5km/l Fuel Efficiency" and user.Fuel_Efficiency < 50:
        user.Fuel_Efficiency += 5
    elif selected_item["name"] == "Refueling Services" or selected_item["name"] == "Environmental-Friendly Refueling Services":
        user.Fuel = 100
    elif selected_item["name"] == "One-Time Extra Cargo capacity":
        user.BoughtExtraCash = True
    else:
        user.BoughtFuelTank = True

    response = {
        "status": "Success",
        "message": f"{selected_item['name']} was successfully purchased.",
    }
    user.update_all()
    return response

def Fuel_Prices(user):
    refuel = 100 - user.Fuel
    response = {
            "Refuel$":refuel*10,
            "RefuelCO2":refuel*10+500,
            "Env-Refuel$":refuel*10+500,
            "Env-RefuelCO2":refuel*10
        }
    return response
"""
from random import randint
from Player_Data import Player
for i in range(0,100,1):
    TestDummy = Player("TEST" + str(i), "EFHK", "TEST", 10000, randint(0,100), randint(0,5000), randint(1,10)*5, False, False, "TEST")
    result = Shop(TestDummy,randint(1,5))
    for j in result:
        print(j)
    print(f"{TestDummy.BoughtFuelTank} {TestDummy.Fuel} {TestDummy.Fuel_Efficiency} {TestDummy.BoughtExtraCash}")
    print("--------------------------------------------")
    
"""