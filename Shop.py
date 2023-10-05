import mysql.connector
connection = mysql.connector.connect(
         host='127.0.0.1',
         port= 3306,
         database='flight_game',
         user='flight_sim',
         password='menudb',
         autocommit=True
         )

# Create a cursor for all interactions with the MariaDB Database
cursor = connection.cursor()
def shop(user):
    print(f"Your current balance: {user.Money}$")
    print(f"Your current CO2 budget: {user.CO2_Budget}")
    print(f"Your current CO2 budget: {user.Fuel}")
    Refuel = 100 - user.Fuel
    items = {
        "+5km/l Fuel Efficiency": (1000, 100, 5),
        "Refueling Services": (Refuel * 10, Refuel * 10 + 500),
        "Environmental-Friendly Refueling Services": (Refuel * 10 + 500, Refuel * 10),
        "One-Time Extra Cargo capacity": (200, 250),
        "One-Time Fuel Drop Tanks": (200, 1000)
    }

    user.purchased_items = {}

    while True:
        print("Available items:")
        for item, price in items.items():
            (moneyprice, CO2_price) = price
            print(f"{item}: {moneyprice}$, {CO2_price} CO2 tokens")

        print("Your purchased items:")
        for item, quantity in user.purchased_items.items():
            print(f"{item}: {quantity}")

        selected_item = input("Enter the item you want to purchase or type 'show' to see your purchased items: ")

        if selected_item == 'show':
            continue

        if selected_item not in items:
            print("Invalid item selection.")
            return False

        (moneyprice, CO2_price, fuel_efficiency_increase) = items[selected_item]

        if user.Money < moneyprice:
            print("You don't have enough money.")
            return False

        if user.CO2_Budget < CO2_price:
            print("Are you sure you want to go into a negative CO2 budget?")
            UsInput = input("Yes/No ")
            if UsInput == "No":
                return False

        user.Money = user.Money - moneyprice
        user.CO2_Budget = user.CO2_Budget - CO2_price
        print(f"Purchase of {selected_item} successful. Your new balance: {user.Money}")

        # Apply the item's effect
        user.Fuel_Efficiency += fuel_efficiency_increase

        # Update purchased items dictionary
        if selected_item in user.purchased_items:
            user.purchased_items[selected_item] += 1
        else:
            user.purchased_items[selected_item] = 1

        update_player(cursor, user)
        return True