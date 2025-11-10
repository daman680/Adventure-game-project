import random
import json
import os
import gamefunctions

MAX_HP = 30

# Global player status
player_status = {"hp": MAX_HP, "luck": 0.1}


def save_game(filename, gold, items, player_status, player_name):
    """
    Save the current game state to a JSON file.

    Parameters:
    - filename (str): Name of the file to save to
    - gold (int): Current gold amount
    - items (dict): Player inventory
    - player_status (dict): Player stats (HP, luck, equipped weapon)
    - player_name (str): Name of the adventurer
    """
    save_data = {
        "gold": gold,
        "items": items,
        "player_status": player_status,
        "player_name": player_name
    }
    with open(filename, "w") as f:
        json.dump(save_data, f, indent=4)
    print(f"Game saved to {filename}.")


def load_game(filename):
    """
    Load a game state from a JSON file.

    Parameters:
    - filename (str): Name of the file to load from

    Returns:
    - tuple: (gold (int), items (dict), player_status (dict), player_name (str))
    """
    with open(filename, "r") as f:
        save_data = json.load(f)
    return (save_data["gold"], save_data["items"],
            save_data["player_status"], save_data["player_name"])


def town_menu(gold, items, player_name):
    """
    Displays the town menu and handles player choices.

    Parameters:
    - gold (int): Current amount of gold the player has
    - items (dict): Current items the player has with quantities
    - player_name (str): Name of the adventurer

    Returns:
    - tuple: (gold after actions, items after actions, player_name)
    """
    while True:
        print(f"\nYou are in town. HP: {player_status['hp']}, Gold: {gold}")
        print("1) Leave town (Fight Monster)")
        print("2) Sleep (Restore HP for 5 Gold)")
        print("3) Visit Shop")
        print("4) Save and Quit")
        print("5) Quit without saving")
        choice = input("Choose an action: ").strip()

        if choice == "1":
            return gold, items, player_name
        elif choice == "2":
            if gold >= 5:
                gold -= 5
                player_status["hp"] = MAX_HP
                print(f"You slept and restored to {MAX_HP} HP. Gold left: {gold}")
            else:
                print("Not enough gold to sleep!")
        elif choice == "3":
            gold, items = visit_shop(gold, items)
        elif choice == "4":
            filename = input("Enter a filename to save your game: ").strip()
            save_game(filename, gold, items, player_status, player_name)
            print("Thanks for playing!")
            exit()
        elif choice == "5":
            print("Thanks for playing!")
            exit()
        else:
            print("Invalid input. Try again.")


def visit_shop(gold, items):
    """
    Handles visiting the shop and purchasing potions, gear, and consumables.
    Gear and consumables appear more often than potions.

    Parameters:
    - gold (int): Player's current gold
    - items (dict): Player's current inventory
        Expected structure: {"potions": {}, "gear": []}

    Returns:
    - tuple: (updated gold, updated items)
    """
    potions = [
        ("Health Potion", (40, 60)),
        ("MP Potion", (30, 50)),
        ("Strength Potion", (100, 130)),
        ("Defense Potion", (90, 120)),
        ("Cloaking Potion", (80, 100)),
        ("Speed Potion", (70, 90))
    ]

    gear_and_consumables = [
        {"name": "Iron Sword", "type": "weapon", "maxDurability": 10, "currentDurability": 10},
        {"name": "Magic Gem", "type": "consumable", "note": "Defeats a monster automatically"}
    ]

    all_items = potions + gear_and_consumables * 3
    item1, item2 = random.sample(all_items, 2)

    def get_price(item):
        if isinstance(item, tuple):
            return round(random.uniform(*item[1]))
        else:
            return random.randint(50, 150)

    item1_price = get_price(item1)
    item2_price = get_price(item2)
    name1 = item1[0] if isinstance(item1, tuple) else item1["name"]
    name2 = item2[0] if isinstance(item2, tuple) else item2["name"]
    gamefunctions.print_shop_menu(name1, item1_price, name2, item2_price)

    print(f"\nYou have {gold} gold.")
    choice = input(f"Which item to buy? ({name1} or {name2} or 'none'): ").strip().lower()
    if choice == "none":
        return gold, items

    quantity = 1
    if isinstance(item1, tuple) or isinstance(item2, tuple):
        try:
            quantity = int(input("How many? "))
        except ValueError:
            quantity = 1

    if choice == name1.lower():
        selected_item = item1
        price = item1_price
        selected_name = name1
    elif choice == name2.lower():
        selected_item = item2
        price = item2_price
        selected_name = name2
    else:
        print("Item not available.")
        return gold, items

    bought, gold = gamefunctions.purchase_item(price, gold, quantity)

    if isinstance(selected_item, tuple):
        items["potions"][selected_name] = items["potions"].get(selected_name, 0) + bought
    else:
        for _ in range(bought):
            items["gear"].append(selected_item.copy())

    print(f"Bought {bought} {selected_name}(s). Gold left: {gold}")
    return gold, items


def monster_fight(monster, items):
    monster_hp = monster["health"]
    player_status.setdefault("equipped_weapon", None)

    print(f"\n⚔️  A wild {monster['name']} appears!")
    print(monster['description'])
    print(f"HP: {monster_hp}, Power: {monster['power']}, Gold: {monster['money']}")

    while monster_hp > 0 and player_status["hp"] > 0:
        print(f"\nYour HP: {player_status['hp']}, Monster HP: {monster_hp}")
        if player_status["equipped_weapon"]:
            weapon = player_status["equipped_weapon"]
            print(f"Equipped weapon: {weapon['name']} (Durability: {weapon['currentDurability']})")
        print("1) Attack")
        print("2) Use Item / Equip Weapon")
        print("3) Run Away")
        action = input("Choose action: ").strip()

        if action == "1":
            damage = random.randint(5, 25)
            if random.random() < player_status["luck"]:
                damage *= 2
                print("Critical Hit!")
            if "Strength Potion" in items["potions"] and items["potions"]["Strength Potion"] > 0:
                damage += 5
                items["potions"]["Strength Potion"] -= 1
                print("Strength Potion boosts your attack!")
            if player_status["equipped_weapon"]:
                damage += 10
                player_status["equipped_weapon"]["currentDurability"] -= 1
                print(f"{player_status['equipped_weapon']['name']} adds +10 damage!")
                if player_status["equipped_weapon"]["currentDurability"] <= 0:
                    print(f"Your {player_status['equipped_weapon']['name']} broke!")
                    items["gear"].remove(player_status["equipped_weapon"])
                    player_status["equipped_weapon"] = None

            monster_hp -= damage
            monster_hp = max(monster_hp, 0)
            print(f"You dealt {damage} damage.")

            monster_damage = monster["power"]
            if "Defense Potion" in items["potions"] and items["potions"]["Defense Potion"] > 0:
                monster_damage = max(monster_damage - 5, 0)
                items["potions"]["Defense Potion"] -= 1
                print("Defense Potion reduces incoming damage!")
            player_status["hp"] -= monster_damage
            player_status["hp"] = max(player_status["hp"], 0)
            print(f"Monster hits you for {monster_damage} damage.")

        elif action == "2":
            print("\nYour potions:")
            for name, qty in items["potions"].items():
                print(f"{name}: {qty}")

            print("\nYour gear/consumables:")
            for i, g in enumerate(items["gear"]):
                print(f"{i+1}) {g['name']} ({g['type']})")

            item_choice = input("Which item to use/equip? ").strip()

            if item_choice in items["potions"] and items["potions"][item_choice] > 0:
                if item_choice == "Health Potion":
                    heal_amount = min(15, MAX_HP - player_status["hp"])
                    player_status["hp"] += heal_amount
                    print(f"Used Health Potion, healed {heal_amount} HP.")
                elif item_choice == "Strength Potion":
                    print("Strength Potion will boost your next attack!")
                items["potions"][item_choice] -= 1
            else:
                found = None
                for g in items["gear"]:
                    if g["name"].lower() == item_choice.lower() and g["type"] == "weapon":
                        found = g
                        break
                if found:
                    player_status["equipped_weapon"] = found
                    print(f"You equipped {found['name']}! (+10 damage per attack)")
                else:
                    for g in items["gear"]:
                        if g["name"].lower() == item_choice.lower() and g["type"] == "consumable":
                            print(f"{g['name']} activated! Monster is instantly defeated!")
                            monster_hp = 0
                            items["gear"].remove(g)
                            break
                    else:
                        print("Item unavailable or none left.")

        elif action == "3":
            print("You ran away!")
            return 0
        else:
            print("Invalid input. Try again.")

        if player_status["hp"] <= 0:
            print("\nYour HP has reached 0. Game Over.")
            return 0

    print(f"\nYou defeated {monster['name']} and collected {monster['money']} gold!")
    return monster["money"]


def main():
    """
    Main game loop including town visits and monster fights, with save/load functionality.
    """
    print("Welcome to the Adventure Game!")
    choice = input("Start a New Game (N) or Load Game (L)? ").strip().upper()

    if choice == "L":
        filename = input("Enter save filename: ").strip()
        if os.path.exists(filename):
            gold, items, loaded_status, player_name = load_game(filename)
            player_status.update(loaded_status)
            print(f"Loaded game from {filename}. Welcome back, {player_name}!")
        else:
            print("Save file not found. Starting new game.")
            gold = random.randint(100, 300)
            items = {"potions": {}, "gear": []}
            player_status["hp"] = MAX_HP
            player_name = input("Enter your name, adventurer: ")
    else:
        gold = random.randint(100, 300)
        items = {"potions": {}, "gear": []}
        player_status["hp"] = MAX_HP
        player_name = input("Enter your name, adventurer: ")

    gamefunctions.print_welcome(player_name, 50)

    while True:
        gold, items, player_name = town_menu(gold, items, player_name)

        print("\nLeaving town...")
        monster = gamefunctions.new_random_monster()
        loot = monster_fight(monster, items)

        if player_status["hp"] <= 0:
            break

        gold += loot


if __name__ == "__main__":
    main()
