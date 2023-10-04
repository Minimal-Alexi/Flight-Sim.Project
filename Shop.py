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
    sql = f"SELECT CO2_BUDGET FROM GAME WHERE ID = {user}"
    cursor.execute(sql)
    result = cursor.fetchone()
    if not result:
        print("Player not found.")
        return

    current_balance = result[0]
    print(f"Your current balance: {current_balance}")
    items = {
        "Speedbooster_5min": 50,
        "Protectingshield_5min": 50,
        "Advanced_engines": 200,
        "Advanced_fuselage": 200,
    }

    print("Available items:")
    for item, price in items.items():
        print(f"{item}: {price} currency")
    selected_item = input("Enter the item you want to purchase: ")
    if selected_item not in items:
        print("Invalid item selection.")
        return

    item_price = items[selected_item]
    if current_balance < item_price:
        print("You don't have enough money.")
        return
    new_balance = current_balance - item_price
    sql = f"UPDATE GAME SET CO2_BUDGET = {new_balance} WHERE USER = {user}"
    cursor.execute(sql)
    connection.commit()
    print(f"Purchase of {selected_item} successful. Your new balance: {new_balance}")
    return True