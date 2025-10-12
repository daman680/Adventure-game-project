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
    max_affordable = startingMoney // itemPrice
    quantity_bought = min(quantityToPurchase, max_affordable)
    money_remaining = startingMoney - (quantity_bought * itemPrice)
    return quantity_bought, money_remaining


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
            "name": "Vulture",
            "description": (
                "You discover a vulture eating the remains of two orcs that appear to have killed each other.\n"
                "They were carrying a chest that contains a small treasure horde. You will need to scare off the\n"
                "vulture before you can take the treasure."
            ),
            "health_range": (1, 3),
            "power_range": (5, 10),
            "money_range": (1000, 1500)
        },
        {
            "name": "Goblin",
            "description": (
                "A small, sneaky creature lurking in the shadows. It might not look dangerous,\n"
                "but it can call reinforcements if threatened.\n"
                "Their daggers can be stolen off of them if you can sneak up on them.\n"
                "Do not let them gang up on you, as that is a quick way to death."
            ),
            "health_range": (30, 50),
            "power_range": (10, 20),
            "money_range": (50, 100)
        },
        {
            "name": "Troll",
            "description": (
                "A large and lumbering beast with regenerative powers. It is slow but very tough.\n"
                "Approach with caution and heavy weapons.\n"
                "If you do manage to take them down, great treasures can almost always be found nearby.\n"
                "They hit hard with their usually heavier clubs or maces. Don't get hit."
            ),
            "health_range": (100, 150),
            "power_range": (15, 30),
            "money_range": (100, 200)
        }
    ]

    monster_choice = random.choice(monsters)
    health = random.randint(*monster_choice["health_range"])
    power = random.randint(*monster_choice["power_range"])
    money = random.randint(*monster_choice["money_range"])

    return {
        "name": monster_choice["name"],
        "description": monster_choice["description"],
        "health": health,
        "power": power,
        "money": money
    }


def print_welcome(name, width):
    """
    Prints a centered welcome message using the supplied name and width.

    Parameters:
    - name (str): Name of the person to welcome.
    - width (int): Total width to center the message within.

    Returns:
    - None
    """
    message = f"Hello, {name}!"
    print(message.center(width))


def print_shop_menu(item1Name, item1Price, item2Name, item2Price):
    """
    Displays a formatted shop menu with two items and their prices.
    Item names are left-aligned (16 characters), and prices are right-aligned (8 characters)
    with two decimal places and a dollar sign. Surrounded by a decorative border.
    """
    item_field_width = 16
    price_field_width = 8

    line1 = f"| {item1Name.ljust(item_field_width)}${item1Price:>{price_field_width - 1}.2f} |"
    line2 = f"| {item2Name.ljust(item_field_width)}${item2Price:>{price_field_width - 1}.2f} |"
    border_top = "/" + "-" * (len(line1) - 2) + "\\"
    border_bottom = "\\" + "-" * (len(line1) - 2) + "/"

    print(border_top)
    print(line1)
    print(line2)
    print(border_bottom)


# Health Potion Purchases
for i in range(3):
    item_price = random.randint(1000, 5000)
    starting_money = random.randint(500, 7000)
    quantity_to_purchase = random.randint(1, 5)

    num_purchased, leftover_money = purchase_item(item_price, starting_money, quantity_to_purchase)
    print(f"Health Potion Price: {item_price}")
    print(f"Starting Gold: {starting_money}")
    print(f"Potions to Buy: {quantity_to_purchase}")
    print(f"Potions Bought: {num_purchased}")
    print(f"Gold Left: {leftover_money}")
    print("-" * 30)

# Monster Encounters
print("\n=== Random Monster Encounters ===")
for i in range(3):
    monster = new_random_monster()
    print(f"Monster #{i+1}: {monster['name']}")
    print(monster['description'])
    print(f"Health: {monster['health']}")
    print(f"Power: {monster['power']}")
    print(f"Money: {monster['money']}")
    print("-" * 40)

# Welcome Messages 
print("\n=== Welcome Messages ===")
print_welcome("Jeff", 20)
print_welcome("Audrey", 30)
print_welcome("Christopher", 40)
print("-" * 40)

# Randomized Potion Shop Menus 
# Potion list with price ranges (min_price, max_price)
potions = [
    ("Health Potion", (40, 60)),
    ("MP Potion", (30, 50)),
    ("Strength Potion", (100, 130)),
    ("Defense Potion", (90, 120)),
    ("Cloaking Potion", (80, 100)),
    ("Speed Potion", (70, 90))
]

print("\n=== Daman's potions shop ===")

for _ in range(3):
    # Pick two different potions
    item1, item2 = random.sample(potions, 2)

    # Generate random prices within their ranges
    item1_price = round(random.uniform(*item1[1]), 2)
    item2_price = round(random.uniform(*item2[1]), 2)

    print_shop_menu(item1[0], item1_price, item2[0], item2_price)
    print()
