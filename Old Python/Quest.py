from random import randint
from Database import get_country_from_ident
def QuestMenu(user,cursor):
    reward1 = 0
    reward2 = 0
    distance1 = 0
    distance2 = 0
    country1 = ""
    country2 = ""
    print("Would you like to pick a quest?")
    if user.quest[0]!=False:
        print("You have already taken the quest!")
        distance1 = user.quest[0][1]
        reward1 = user.quest[0][0]
        travelled1 = user.quest[0][2]
        country1 = user.quest[0][3]
        print(f"You have to go to {distance1} local {country1} airfields. if you do so, the government will subsidize you with {reward1}$.")
        print(f"So far, you have travelled to {travelled1} airports. Nice! :3")
    else:
        distance1 = randint(5, 8)
        reward1 = randint(1000, 3500)
        if user.BoughtExtraCash == True:
            reward1 = reward1 + 750
        print(f"1 - You have to go to {distance1} local airfields. if you do so, the government will subsidize you with {reward1}$. "
              f"It costs 500 CO2 tokens to load your plane.")
    if user.quest[1]!=False:
        print("You have already taken the quest!")
        distance2 = user.quest[1][1]
        reward2 = user.quest[1][0]
        travelled2 = user.quest[1][2]
        country2 = user.quest[1][3]
        print(f"You have to go to {distance2} international airfields (that are not {country2}. if you do so, the government will subsidize you with {reward1}$.")
        print(f"So far, you have travelled to {travelled2} airports. Nice! :3")
    else:
        if user.BoughtExtraCash == True:
            reward1 = reward1 + 750
        distance2 = randint(1, 3)
        reward2 = randint(750, 5000)
        print(
            f"2 - You have to go to {distance2} international airfields. if you do so, the government will subsidize you with {reward2}$. "
            f"It costs 750 CO2 tokens to load your plane.")
    print("3 - Would you like to plant some trees? (-1500$,+1000 CO2)")
    print("4 - Quit")
    UsInput = int(input("Which quest would you like to pick?: "))
    if UsInput == 1 and user.quest[0]==False:
        country1 = get_country_from_ident(user.location,cursor)[0]
        #Yes, we are creating a list in a list. Reward1 is how much money the player gets. distance1 is the goal distance they have to travel.
        # 0 is the distance they've travelled, and country 1 is the country they have the quest in.
        user.quest[0] = [reward1,distance1,0,country1]
        user.CO2_Budget = user.CO2_Budget - 500
    elif UsInput == 2 and user.quest[1]==False:
        country2 = get_country_from_ident(user.location, cursor)[0]
        user.quest[1] = [reward2, distance2, 0, country2]
        user.CO2_Budget = user.CO2_Budget - 750
    elif UsInput == 3:
        user.CO2_Budget = user.CO2_Budget + 1000
        user.Money = user.Money - 1500
    elif UsInput != 4:
        print("Invalid choice,try again.")
        QuestMenu()
    extracash = False
    #print(user.quest)

def CheckQuest(user,cursor):
    #Thos function checks,and updates players progress on their own quests.
    if user.quest[0]!=False:
        if get_country_from_ident(user.location,cursor)[0] == user.quest[0][3]:
            user.quest[0][2] = user.quest[0][2]+1
        if user.quest[0][2]==user.quest[0][1]:
            user.Money=user.Money+user.quest[0][0]
            print(f"Congrats, you have finished your quest, you've now earned {user.quest[0][0]}$")
            user.quest[0]=False
    if user.quest[1]!=False:
        if get_country_from_ident(user.location,cursor)[0] != user.quest[1][3]:
            user.quest[1][2] = user.quest[1][2]+1
        if user.quest[1][2]==user.quest[1][1]:
            user.Money=user.Money+user.quest[1][0]
            print(f"Congrats, you have finished your quest, you've now earned {user.quest[1][0]}$")
            user.quest[1]=False