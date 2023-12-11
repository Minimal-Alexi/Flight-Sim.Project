import json
from random import randint
from Database import get_country_from_ident
from Player_Data import Player

def quest(user, questID):
    if questID == 3:
        if user.Money>=1500:
            user.Money -= 1500
            user.CO2_Budget += 1000
            response = {
                "status": "Success",
                "message": f"Quest : Succesfully planted trees! +1000 CO2 Tokens -1500€.",
            }
        else:
            response = {
                "status": "Failed",
                "message": f"Can't even afford tree saplings..?",
            }
    else:
        # list of quests with their rewards ~Ash
        quests = {
            1: {"name": "Local Quest", "reward": 0, "distance": 0, "cost": 500, "CO2_reward": 0},
            2: {"name": "International Quest", "reward": 0, "distance": 0, "cost": 750, "CO2_reward": 0},
        }
        # gets the selected quest ~Ash
        selected_quest = quests[questID]
        # adjusts player variables based on the picked quest
        # logic from Quest.py ~Ash
        if questID == 1:
            # checks if the user has already taken the quest
            # we can make it so the button disappears after you pick a quest but idk how so this for now ~Ash
            if user.Quest[questID - 1] is not False:
                response = {"status": "Error", "message": "You have already taken this quest."}
                return response
            selected_quest["distance"] = randint(5, 8)
            selected_quest["reward"] = randint(1000, 3500)
            if user.BoughtExtraCash:
                selected_quest["reward"] += 750
        elif questID == 2:
            if user.Quest[questID - 1] is not False:
                response = {"status": "Error", "message": "You have already taken this quest."}
                return response
            selected_quest["distance"] = randint(1, 3)
            selected_quest["reward"] = randint(750, 5000)
            if user.BoughtExtraCash:
                selected_quest["reward"] += 750
        selected_quest["cost"] = 750
        selected_quest["CO2_reward"] = 0
        # getting Country ~Ash
        country = get_country_from_ident(user.location)[0]
        user.Quest[questID - 1] = [selected_quest["reward"], selected_quest["distance"], 0, country]
        user.CO2_Budget -= selected_quest["cost"]
        # updates for user quest data and adjusting co2 budget ~Ash
        response = {
                "status": "Success",
                "message": f"Quest : {selected_quest['name']} has successfully started. You have to travel to {selected_quest['distance']} airports. The reward will be {selected_quest['reward']}",
            }
    user.update_all()
    return response