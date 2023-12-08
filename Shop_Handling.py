import json
# def Shop (user,ItemID)
# {
#     list of items to purchase (you can just have their prices)
#     check which item the user purchases
#     check if user has money
#     adjust player variables based on item
#     return JSON response about purchase.
#     if successful jsonify(user.json,200)
#     else jsonify(400)
# }



def Shop(user, ItemID):
    items = {
        1: {"name": "+5km/l Fuel Efficiency", "money_price": 1000, "CO2_price": 100},
        2: {"name": "Refueling Services", "money_price": 10, "CO2_price": 10}
    }

    # check which item the user purchases
    selected_item = items[ItemID]

    # check if user has money
    if user.Money < selected_item["money_price"]:
        response = {"status": "Error", "message": "You don't have enough money."}
        return json.dumps(response), 400

    # adjust player variables based on item
    user.Money -= selected_item["money_price"]
    user.CO2_Budget -= selected_item["CO2_price"]

    # item's effect on player variables
    if selected_item["name"] == "+5km/l Fuel Efficiency":
        user.Fuel_Efficiency += 5
    elif selected_item["name"] == "Refueling Services":
        user.Fuel += 10

    # successful jsonify(user.json, 200)
    response = {
        "status": "Success",
        "message": f"{selected_item['name']} was successfully purchased.",
    }
    return json.dumps(response), 200
