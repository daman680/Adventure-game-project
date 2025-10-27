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
    Handles visiting the shop and purchasing potions.

    Parameters:
    - gold (int): Player's current gold
    - items (dict): Player's current items

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
    item1, item2 = random.sample(potions, 2)
    item1_price = round(random.uniform(*item1[1]))
    item2_price = round(random.uniform(*item2[1]))
    gamefunctions.print_shop_menu(item1[0], item1_price, item2[0], item2_price)

    print(f"\nYou have {gold} gold.")
    choice = input(f"Which item to buy? ({item1[0]} or {item2[0]} or 'none'): ").strip().lower()
    if choice == "none":
        return gold, items
    quantity = int(input("How many? "))

    if choice == item1[0].lower():
        price = item1_price
        name = item1[0]
    elif choice == item2[0].lower():
        price = item2_price
        name = item2[0]
    else:
        print("Item not available.")
        return gold, items

    bought, gold = gamefunctions.purchase_item(price, gold, quantity)
    items[name] = items.get(name, 0) + bought
    print(f"Bought {bought} {name}(s). Gold left: {gold}")
    return gold, items


def monster_fight(monster, items):
    """
    Handles the monster fight loop.

    Parameters:
    - monster (dict): Monster info
    - items (dict): Player's items

    Returns:
    - int: Gold gained from defeating the monster (0 if player dies)
    """
    monster_hp = monster["health"]
    print(f"\n⚔️  A wild {monster['name']} appears!")
    print(monster['description'])
    print(f"HP: {monster_hp}, Power: {monster['power']}, Gold: {monster['money']}")

    while monster_hp > 0 and player_status["hp"] > 0:
        print(f"\nYour HP: {player_status['hp']}, Monster HP: {monster_hp}")
        print("1) Attack")
        print("2) Use Item")
        print("3) Run Away")
        action = input("Choose action: ").strip()

        if action == "1":
            damage = random.randint(5, 25)
            if random.random() < player_status["luck"]:
                damage *= 2
                print("Critical Hit!")
            if "Strength Potion" in items and items["Strength Potion"] > 0:
                damage += 5
                items["Strength Potion"] -= 1
                print("Strength Potion boosts your attack!")
            monster_hp -= damage
            monster_hp = max(monster_hp, 0)
            print(f"You dealt {damage} damage.")

            monster_damage = monster["power"]
            if "Defense Potion" in items and items["Defense Potion"] > 0:
                monster_damage = max(monster_damage - 5, 0)
                items["Defense Potion"] -= 1
                print("Defense Potion reduces incoming damage!")
            player_status["hp"] -= monster_damage
            player_status["hp"] = max(player_status["hp"], 0)
            print(f"Monster hits you for {monster_damage} damage.")
        elif action == "2":
            print("\nYour items:")
            for name, qty in items.items():
                print(f"{name}: {qty}")
            item_choice = input("Which item to use? ").strip()
            if item_choice in items and items[item_choice] > 0:
                if item_choice == "Health Potion":
                    heal_amount = min(15, MAX_HP - player_status["hp"])
                    player_status["hp"] += heal_amount
                    print(f"Used Health Potion, healed {heal_amount} HP.")
                else:
                    print(f"{item_choice} will help in future fights.")
                items[item_choice] -= 1
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
    items = {}
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
