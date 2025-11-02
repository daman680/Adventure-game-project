import random
import gamefunctions

MAX_HP = 30

# Global player status
player_status = {"hp": MAX_HP, "luck": 0.1}


def town_menu(gold, items):
    """
    Displays the town menu and handles player choices.

    Parameters:
    - gold (int): Current amount of gold the player has
    - items (dict): Current items the player has with quantities

    Returns:
    - tuple: (gold after actions, items after actions)
    """
    while True:
        print(f"\nYou are in town. HP: {player_status['hp']}, Gold: {gold}")
        print("1) Leave town (Fight Monster)")
        print("2) Sleep (Restore HP for 5 Gold)")
        print("3) Visit Shop")
        print("4) Quit")
        choice = input("Choose an action: ").strip()

        if choice == "1":
            return gold, items  # leave town
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
    import random
    import gamefunctions

    # Potions (less frequent)
    potions = [
        ("Health Potion", (40, 60)),
        ("MP Potion", (30, 50)),
        ("Strength Potion", (100, 130)),
        ("Defense Potion", (90, 120)),
        ("Cloaking Potion", (80, 100)),
        ("Speed Potion", (70, 90))
    ]

    # Gear / consumables (more frequent)
    gear_and_consumables = [
        {"name": "Iron Sword", "type": "weapon", "maxDurability": 10, "currentDurability": 10},
        {"name": "Magic Gem", "type": "consumable", "note": "Defeats a monster automatically"}
    ]

    # Weight gear more heavily by duplicating it in the pool
    all_items = potions + gear_and_consumables * 3  # gear 3x more likely than potions

    # Randomly pick two items
    item1, item2 = random.sample(all_items, 2)

    # Determine prices
    def get_price(item):
        if isinstance(item, tuple):  # potion
            return round(random.uniform(*item[1]))
        else:  # gear or consumable
            return random.randint(50, 150)

    item1_price = get_price(item1)
    item2_price = get_price(item2)

    # Print shop menu
    name1 = item1[0] if isinstance(item1, tuple) else item1["name"]
    name2 = item2[0] if isinstance(item2, tuple) else item2["name"]
    gamefunctions.print_shop_menu(name1, item1_price, name2, item2_price)

    print(f"\nYou have {gold} gold.")
    choice = input(f"Which item to buy? ({name1} or {name2} or 'none'): ").strip().lower()
    if choice == "none":
        return gold, items

    # Quantity (only for potions)
    quantity = 1
    if isinstance(item1, tuple) or isinstance(item2, tuple):
        try:
            quantity = int(input("How many? "))
        except ValueError:
            quantity = 1

    # Determine chosen item
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

    # Purchase logic
    bought, gold = gamefunctions.purchase_item(price, gold, quantity)

    if isinstance(selected_item, tuple):  # potion
        items["potions"][selected_name] = items["potions"].get(selected_name, 0) + bought
    else:  # gear / consumable
        for _ in range(bought):
            items["gear"].append(selected_item.copy())  # copy to keep separate durability

    print(f"Bought {bought} {selected_name}(s). Gold left: {gold}")
    return gold, items

def monster_fight(monster, items):
    monster_hp = monster["health"]
    player_status.setdefault("equipped_weapon", None)  # Track equipped weapon

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
            # Base attack damage
            damage = random.randint(5, 25)
            # Critical hit
            if random.random() < player_status["luck"]:
                damage *= 2
                print("Critical Hit!")
            # Potion boosts
            if "Strength Potion" in items["potions"] and items["potions"]["Strength Potion"] > 0:
                damage += 5
                items["potions"]["Strength Potion"] -= 1
                print("Strength Potion boosts your attack!")

            # Weapon damage
            if player_status["equipped_weapon"]:
                damage += 10
                player_status["equipped_weapon"]["currentDurability"] -= 1
                print(f"{player_status['equipped_weapon']['name']} adds +10 damage!")
                # Break sword if durability is 0
                if player_status["equipped_weapon"]["currentDurability"] <= 0:
                    print(f"Your {player_status['equipped_weapon']['name']} broke!")
                    items["gear"].remove(player_status["equipped_weapon"])
                    player_status["equipped_weapon"] = None

            monster_hp -= damage
            monster_hp = max(monster_hp, 0)
            print(f"You dealt {damage} damage.")

            # Monster attacks
            monster_damage = monster["power"]
            if "Defense Potion" in items["potions"] and items["potions"]["Defense Potion"] > 0:
                monster_damage = max(monster_damage - 5, 0)
                items["potions"]["Defense Potion"] -= 1
                print("Defense Potion reduces incoming damage!")
            player_status["hp"] -= monster_damage
            player_status["hp"] = max(player_status["hp"], 0)
            print(f"Monster hits you for {monster_damage} damage.")

        elif action == "2":
            # Show potions
            print("\nYour potions:")
            for name, qty in items["potions"].items():
                print(f"{name}: {qty}")

            # Show gear
            print("\nYour gear/consumables:")
            for i, g in enumerate(items["gear"]):
                print(f"{i+1}) {g['name']} ({g['type']})")

            item_choice = input("Which item to use/equip? ").strip()

            # Potions
            if item_choice in items["potions"] and items["potions"][item_choice] > 0:
                if item_choice == "Health Potion":
                    heal_amount = min(15, MAX_HP - player_status["hp"])
                    player_status["hp"] += heal_amount
                    print(f"Used Health Potion, healed {heal_amount} HP.")
                elif item_choice == "Strength Potion":
                    print("Strength Potion will boost your next attack!")
                items["potions"][item_choice] -= 1

            else:
                # Gear equip
                found = None
                for g in items["gear"]:
                    if g["name"].lower() == item_choice.lower() and g["type"] == "weapon":
                        found = g
                        break
                if found:
                    player_status["equipped_weapon"] = found
                    print(f"You equipped {found['name']}! (+10 damage per attack)")
                else:
                    # Check consumables
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
    Main game loop including town visits and monster fights.
    """
    player_name = input("Enter your name, adventurer: ")
    gamefunctions.print_welcome(player_name, 50)

    gold = random.randint(100, 300)
    items = {
    "potions": {},
    "gear": []
    }
    player_status["hp"] = MAX_HP

    while True:
        gold, items = town_menu(gold, items)

        print("\nLeaving town...")
        monster = gamefunctions.new_random_monster()
        loot = monster_fight(monster, items)

        if player_status["hp"] <= 0:
            break  # Exit loop if player dies

        gold += loot


if __name__ == "__main__":
    main()
# screwed up commit, forcing new commit
