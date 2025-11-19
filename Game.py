import random
import json
import os
import pygame
import gamefunctions

MAX_HP = 30
player_status = {"hp": MAX_HP, "luck": 0.1}


def save_game(filename, gold, items, player_status, player_name):
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
    with open(filename, "r") as f:
        save_data = json.load(f)
    return (save_data["gold"], save_data["items"],
            save_data["player_status"], save_data["player_name"],
            save_data.get("map_state", {}))


def run_map(map_state):
    """
    Runs the map exploration using pygame. Player can move on a 10x10 grid.
    Town tile is green, monster tile is red. Moving to the monster triggers a fight.
    Moving back to the town tile after moving returns to town menu.
    """
    pygame.init()
    screen = pygame.display.set_mode((320, 320))
    pygame.display.set_caption("Adventure Map")
    clock = pygame.time.Clock()

    player_x, player_y = map_state.get("player_pos", [0, 0])
    monster_pos = map_state.get("monster_pos", [random.randint(0, 9), random.randint(0, 9)])
    town_pos = [0, 0]

    # Ensure monster does not spawn on town tile
    if monster_pos == town_pos:
        while monster_pos == town_pos:
            monster_pos = [random.randint(0, 9), random.randint(0, 9)]

    running = True
    moved = False
    action = "none"

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                action = "quit"
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and player_y > 0:
                    player_y -= 1
                    moved = True
                elif event.key == pygame.K_DOWN and player_y < 9:
                    player_y += 1
                    moved = True
                elif event.key == pygame.K_LEFT and player_x > 0:
                    player_x -= 1
                    moved = True
                elif event.key == pygame.K_RIGHT and player_x < 9:
                    player_x += 1
                    moved = True

        # Draw map
        screen.fill((0, 0, 0))
        for i in range(10):
            for j in range(10):
                rect = pygame.Rect(i*32, j*32, 32, 32)
                pygame.draw.rect(screen, (255, 255, 255), rect, 1)

        pygame.draw.circle(screen, (0, 255, 0), (town_pos[0]*32+16, town_pos[1]*32+16), 10)
        pygame.draw.circle(screen, (255, 0, 0), (monster_pos[0]*32+16, monster_pos[1]*32+16), 10)
        pygame.draw.rect(screen, (0, 0, 255), pygame.Rect(player_x*32, player_y*32, 32, 32))

        pygame.display.flip()
        clock.tick(10)

        player_pos = [player_x, player_y]

        if moved:
            if player_pos == monster_pos:
                action = "fight"
                running = False
            elif player_pos == town_pos:
                action = "town"
                running = False

    pygame.quit()
    map_state["player_pos"] = [player_x, player_y]
    map_state["monster_pos"] = monster_pos
    return action, map_state


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


def town_menu(gold, items, player_name, map_state):
    """
    Handles town menu actions. Opens map exploration and persists map state.
    """
    while True:
        print(f"\nYou are in town. HP: {player_status['hp']}, Gold: {gold}")
        print("1) Leave town (Explore Map)")
        print("2) Sleep (Restore HP for 5 Gold)")
        print("3) Visit Shop")
        print("4) Save and Quit")
        print("5) Quit without saving")
        choice = input("Choose an action: ").strip()

        if choice == "1":
            action, map_state = run_map(map_state)
            if action == "town":
                continue
            elif action == "fight":
                return gold, items, player_name, map_state, "fight"
            elif action == "quit":
                exit()
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
    Handles shop interaction with random items.
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


def main():
    print("Welcome to the Adventure Game!")
    choice = input("Start a New Game (N) or Load Game (L)? ").strip().upper()

    if choice == "L":
        filename = input("Enter save filename: ").strip()
        if os.path.exists(filename):
            gold, items, loaded_status, player_name, loaded_map = load_game(filename)
            player_status.update(loaded_status)
            map_state = loaded_map
            print(f"Loaded game from {filename}. Welcome back, {player_name}!")
        else:
            print("Save file not found. Starting new game.")
            gold = random.randint(100, 300)
            items = {"potions": {}, "gear": []}
            player_status["hp"] = MAX_HP
            player_name = input("Enter your name, adventurer: ")
            map_state = {}
    else:
        gold = random.randint(100, 300)
        items = {"potions": {}, "gear": []}
        player_status["hp"] = MAX_HP
        player_name = input("Enter your name, adventurer: ")
        map_state = {}

    gamefunctions.print_welcome(player_name, 50)

    while True:
        gold, items, player_name, map_state, action = town_menu(gold, items, player_name, map_state)
        if action == "fight":
            monster = gamefunctions.new_random_monster()
            loot = monster_fight(monster, items)
            if player_status["hp"] <= 0:
                break
            gold += loot


if __name__ == "__main__":
    main()
