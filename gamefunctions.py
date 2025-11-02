import random

def purchase_item(itemPrice, startingMoney, quantityToPurchase=1):
    """
    Determines how many health potions a player can afford to purchase 
    and how much money remains afterward.

    Parameters:
    - itemPrice (int): The price of one health potion.
    - startingMoney (int): The total money the player has before purchasing.
    - quantityToPurchase (int): Desired number of health potions to buy (default is 1).

    Returns:
    - tuple: (quantity_bought (int), money_remaining (int))
    """
    totalCost = itemPrice * quantityToPurchase
    if totalCost <= startingMoney:
        return quantityToPurchase, startingMoney - totalCost
    else:
        maxAffordable = startingMoney // itemPrice
        return maxAffordable, startingMoney - (maxAffordable * itemPrice)


def new_random_monster():
    """
    Creates and returns a randomly selected monster with randomized stats.

    Returns:
    - dict: {
        'name': str,
        'description': str,
        'health': int,
        'power': int,
        'money': int
    }
    """
    monsters = [
        {
            "name": "Goblin",
            "description": "A small, sneaky creature.",
            "health": random.randint(10, 20),
            "power": random.randint(5, 15),
            "money": random.randint(10, 50)
        },
        {
            "name": "Vulture",
            "description": "A vicious bird of prey.",
            "health": random.randint(15, 25),
            "power": random.randint(5, 10),
            "money": random.randint(5, 30)
        },
        {
            "name": "Troll",
            "description": "A huge, brutish monster.",
            "health": random.randint(40, 60),
            "power": random.randint(15, 25),
            "money": random.randint(100, 400)
        }
    ]
    return random.choice(monsters)


def print_welcome(name, width):
    """
    Prints a centered welcome message using the supplied name and width.

    Parameters:
    - name (str): Name of the person to welcome.
    - width (int): Total width to center the message within.

    Returns:
    - None
    """
    welcome_message = f"Welcome, {name}, to the adventure!"
    print("\n" + welcome_message.center(width, "="))


def print_shop_menu(item1, price1, item2, price2):
    """
    Displays a formatted shop menu with two items and their prices.
    Item names are left-aligned (16 characters), and prices are right-aligned (8 characters)
    with two decimal places and a dollar sign. Surrounded by a decorative border.

    Parameters:
    - item1 (str): Name of first item
    - price1 (int): Price of first item
    - item2 (str): Name of second item
    - price2 (int): Price of second item

    Returns:
    - None
    """
    border = "=" * 34
    print(f"\n{border}")
    print(f"{item1:<16}{price1:>8} gold")
    print(f"{item2:<16}{price2:>8} gold")
    print(f"{border}\n")
 
def get_price(item):
    if isinstance(item, tuple):  # potion tuple
        return round(random.uniform(*item[1]))
    else:  # gear or consumable dictionary
        return random.randint(50, 150)

