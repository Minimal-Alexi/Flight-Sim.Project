import json
from random import randint
from Database import get_country_from_ident
from GoogleMaps_API_Feeder import cursor


def quest(user, questID):
    # list of quests with their rewards
    quests = {
        1: {"name": "+5km/l Fuel Efficiency", "reward": 0, "distance": 0, "cost": 500, "CO2_reward": 0},
        2: {"name": "One-Time Extra Cargo capacity", "reward": 0, "distance": 0, "cost": 750, "CO2_reward": 0},
        3: {"name": "Tree Planting Quest", "reward": -1500, "CO2_reward": 1000},
    }

    # gets the selected quest
    selected_quest = quests[questID]

    # checks if the user has already taken the quest
    # we can make it so the button disappears after you pick a quest but idk how so this for now
    if user.Quest[questID - 1] is not False:
        response = {"status": "Error", "message": "You have already taken this quest."}
        return json.dumps(response), 400

    # adjusts player variables based on the picked quest
    # logic from Quest.py
    if questID == 1 or questID == 2:
        if questID == 1:
            selected_quest["distance"] = randint(5, 8)
            selected_quest["reward"] = randint(1000, 3500)
            if user.BoughtExtraCash:
                selected_quest["reward"] += 750
        elif questID == 2:
            selected_quest["distance"] = randint(1, 3)
            selected_quest["reward"] = randint(750, 5000)
            if user.BoughtExtraCash:
                selected_quest["reward"] += 750

        selected_quest["cost"] = 750
        selected_quest["CO2_reward"] = 0

    if questID == 3:
        selected_quest["CO2_reward"] = 1000
        selected_quest["reward"] = -1500

    # getting Country
    country = get_country_from_ident(user.location, cursor)[0]

    # updates for user quest data and adjusting co2 budget
    user.Quest[questID - 1] = [selected_quest["reward"], selected_quest["distance"], 0, country]
    user.CO2_Budget -= selected_quest["cost"]
    user.CO2_Budget += selected_quest["CO2_reward"]

    # adjusting user money based on the reward
    user.Money += selected_quest["reward"]

    # successful jsonify(user.json, 200)
    response = {
        "status": "Success",
        "message": f"Quest :{selected_quest['name']} has successfully started.",
    }
    return json.dumps(response), 200
