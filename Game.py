import random
import json
import os
import pygame
import gamefunctions

MAX_HP = 30
player_status = {"hp": MAX_HP, "luck": 0.1}


def save_game(filename, gold, items, player_status, player_name, map_state):
    save_data = {
        "gold": gold,
        "items": items,
        "player_status": player_status,
        "player_name": player_name,
        "map_state": map_state
    }
    with open(filename, "w") as f:
        json.dump(save_data, f, indent=4)
    print(f"Game saved to {filename}.")


def load_game(filename):
    with open(filename, "r") as f:
        save_data = json.load(f)
    return (
        save_data["gold"],
        save_data["items"],
        save_data["player_status"],
        save_data["player_name"],
        save_data.get("map_state", {}),
    )


def run_map(map_state):
    """
    Runs the map exploration using pygame with persistent monsters.
    Player moves with arrow keys. Town tile is green. Monsters are color-coded:
    Goblin=green, Vulture=yellow, Troll=dark green.
    Returns (action:str, updated_map_state:dict)
    """
    pygame.init()
    TILE_SIZE = 32
    GRID_SIZE = 10
    SCREEN_SIZE = GRID_SIZE * TILE_SIZE
    screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
    pygame.display.set_caption("Adventure Map")
    clock = pygame.time.Clock()

    if "player_pos" not in map_state:
        map_state["player_pos"] = [0, 0]
    if "town_pos" not in map_state:
        map_state["town_pos"] = [0, 0]
    if "monsters" not in map_state:
        monsters = []
        while len(monsters) < 2:
            m = gamefunctions.new_random_monster()
            x, y = random.randint(0, 9), random.randint(0, 9)
            if [x, y] != map_state["player_pos"] and [x, y] != map_state["town_pos"]:
                m["pos"] = [x, y]
                m["alive"] = True
                monsters.append(m)
        map_state["monsters"] = monsters

    player_pos = map_state["player_pos"]
    town_pos = map_state["town_pos"]
    monsters = map_state["monsters"]

    running = True
    move_counter = 0
    action = None

    while running:
        screen.fill((0, 0, 0))

        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                pygame.draw.rect(screen, (50, 50, 50), rect, 1)

        pygame.draw.circle(
            screen,
            (0, 255, 0),
            (town_pos[0] * TILE_SIZE + TILE_SIZE // 2, town_pos[1] * TILE_SIZE + TILE_SIZE // 2),
            TILE_SIZE // 2 - 2,
        )

        for m in monsters:
            if m["alive"]:
                color = (0, 255, 0) if m["name"] == "Goblin" else (255, 255, 0) if m["name"] == "Vulture" else (0, 100, 0)
                pygame.draw.circle(
                    screen,
                    color,
                    (m["pos"][0] * TILE_SIZE + TILE_SIZE // 2, m["pos"][1] * TILE_SIZE + TILE_SIZE // 2),
                    TILE_SIZE // 2 - 2,
                )

        pygame.draw.rect(
            screen,
            (0, 0, 255),
            pygame.Rect(player_pos[0] * TILE_SIZE, player_pos[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE),
        )

        pygame.display.flip()
        clock.tick(10)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return "quit", map_state
            elif event.type == pygame.KEYDOWN:
                moved = False
                if event.key == pygame.K_UP and player_pos[1] > 0:
                    player_pos[1] -= 1
                    moved = True
                elif event.key == pygame.K_DOWN and player_pos[1] < GRID_SIZE - 1:
                    player_pos[1] += 1
                    moved = True
                elif event.key == pygame.K_LEFT and player_pos[0] > 0:
                    player_pos[0] -= 1
                    moved = True
                elif event.key == pygame.K_RIGHT and player_pos[0] < GRID_SIZE - 1:
                    player_pos[0] += 1
                    moved = True

                if moved:
                    move_counter += 1
                    for m in monsters:
                        if m["alive"] and player_pos == m["pos"]:
                            action = "fight"
                            running = False
                            break

                    if player_pos == town_pos:
                        action = "town"
                        running = False

                    if move_counter % 3 == 0:
                        for m in monsters:
                            if not m["alive"]:
                                continue
                            directions = [[0,1],[0,-1],[1,0],[-1,0]]
                            dx, dy = random.choice(directions)
                            new_x = max(0, min(9, m["pos"][0]+dx))
                            new_y = max(0, min(9, m["pos"][1]+dy))
                            if [new_x, new_y] != player_pos and [new_x, new_y] != town_pos and all([new_x,new_y] != mm["pos"] for mm in monsters if mm != m and mm["alive"]):
                                m["pos"] = [new_x, new_y]

    map_state["player_pos"] = player_pos
    map_state["monsters"] = monsters
    return action, map_state


def monster_fight(monster_dict, items):
    monster_hp = monster_dict["health"]
    player_status.setdefault("equipped_weapon", None)

    print(f"\n⚔️  A wild {monster_dict['name']} appears!")
    print(monster_dict['description'])
    print(f"HP: {monster_hp}, Power: {monster_dict['power']}, Gold: {monster_dict['money']}")

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

            monster_damage = monster_dict["power"]
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

    print(f"\nYou defeated {monster_dict['name']} and collected {monster_dict['money']} gold!")
    return monster_dict["money"]


def town_menu(gold, items, player_name, map_state):
    while True:
        print(f"\nYou are in town. HP: {player_status['hp']}, Gold: {gold}")
        print("="*40)
        print("1) Leave town (Explore Map)")
        print("2) Sleep (Restore HP for 5 Gold)")
        print("3) Visit Shop")
        print("4) Save and Quit")
        print("5) Quit without saving")
        print("="*40)
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
            gold, items = gamefunctions.visit_shop(gold, items)
        elif choice == "4":
            filename = input("Enter a filename to save your game: ").strip()
            save_game(filename, gold, items, player_status, player_name, map_state)
            print("Thanks for playing!")
            exit()
        elif choice == "5":
            print("Thanks for playing!")
            exit()
        else:
            print("Invalid input. Try again.")


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
            monsters_alive = [m for m in map_state["monsters"] if m["alive"] and m["pos"] == map_state["player_pos"]]
            if monsters_alive:
                m = monsters_alive[0]
                loot = monster_fight(m, items)
                if player_status["hp"] <= 0:
                    break
                gold += loot
                m["alive"] = False
                new_monster = gamefunctions.new_random_monster()
                while True:
                    x, y = random.randint(0, 9), random.randint(0, 9)
                    if [x, y] != map_state["player_pos"] and [x, y] != map_state["town_pos"] and all([x, y] != mm["pos"] for mm in map_state["monsters"] if mm["alive"]):
                        new_monster["pos"] = [x, y]
                        new_monster["alive"] = True
                        map_state["monsters"].append(new_monster)
                        break


if __name__ == "__main__":
    main()
