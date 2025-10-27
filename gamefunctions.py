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


def fight_monster(player):
    """
    Handles a fight between the player and a randomly generated monster.

    Parameters:
    - player (dict): Dictionary containing player stats, e.g., {'name': str, 'hp': int, 'gold': int}.

    The function runs a fight loop where the player can choose to attack or run.
    Player HP is reduced based on monster attacks, and gold is gained if the monster is defeated.

    Returns:
    - None: Updates the player dictionary directly.
    """
    monster = new_random_monster()
    print(f"\n⚔️  A wild {monster['name']} appears!")
    print(monster['description'])
    print(f"Health: {monster['health']}, Power: {monster['power']}, Gold: {monster['money']}")

    while player['hp'] > 0 and monster['health'] > 0:
        print("\n1) Attack")
        print("2) Run")
        action = input("Choose your action: ").strip()

        if action == "1":
            # Simple combat: player deals random damage 5-15
            player_damage = random.randint(5, 15)
            monster['health'] -= player_damage
            print(f"\nYou hit the {monster['name']} for {player_damage} damage!")

            if monster['health'] <= 0:
                print(f"\nYou defeated the {monster['name']}!")
                player['gold'] += monster['money']
                print(f"You found {monster['money']} gold. Total gold: {player['gold']}")
                break

            # Monster attacks
            monster_damage = random.randint(1, monster['power'])
            player['hp'] -= monster_damage
            print(f"The {monster['name']} hits you for {monster_damage} damage! Your HP: {player['hp']}")

        elif action == "2":
            print(f"\nYou ran away from the {monster['name']}.")
            break
        else:
            print("Unrecognized command. Please choose 1 or 2.")


def sleep(player):
    """
    Restores the player's HP at the cost of gold.

    Parameters:
    - player (dict): Dictionary containing player stats, e.g., {'name': str, 'hp': int, 'gold': int}.

    The function checks if the player has at least 5 gold to pay for sleep.
    If so, restores HP to full (30) and deducts gold.
    If not enough gold, prints a message and does not restore HP.

    Returns:
    - None: Updates the player dictionary directly.
    """
    cost = 5
    if player['gold'] >= cost:
        player['hp'] = 30
        player['gold'] -= cost
        print(f"\nYou slept and restored your HP to {player['hp']}. Gold remaining: {player['gold']}")
    else:
        print("\nNot enough gold to sleep. You need 5 gold.")
# updated to add two new functions for game.py to use
