import random
import json
import os
import pygame
import gamefunctions


MAX_HP = 30
player_status = {"hp": MAX_HP, "luck": 0.1}


def load_sprite(path, fallback_color, size):
    """
    Attempts to load a sprite from the given path.
    Falls back to a solid-color surface if the file cannot be loaded.

    Parameters:
        path (str): The file path to the image.
        fallback_color (tuple): RGB color to use if the image fails to load.
        size (int): Width/height of the returned square surface.

    Returns:
        pygame.Surface: Loaded image or fallback surface.
    """
    try:
        img = pygame.image.load(path)
        return pygame.transform.scale(img, (size, size))
    except Exception:
        surf = pygame.Surface((size, size))
        surf.fill(fallback_color)
        return surf


def save_game(filename, gold, items, player_status, player_name, map_state):
    """
    Saves player data, inventory, status, and map state to a file.

    Parameters:
        filename (str): Name of file to save to.
        gold (int): Player gold.
        items (dict): Inventory structure.
        player_status (dict): Stats such as hp and luck.
        player_name (str): Name of the player.
        map_state (dict): Positions of monsters, player, and town.

    Returns:
        None
    """
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
    """
    Loads game data from a file.

    Parameters:
        filename (str): Name of file to load.

    Returns:
        tuple: gold, items, player_status, player_name, map_state
    """
    with open(filename, "r") as f:
        save_data = json.load(f)
    return (
        save_data["gold"],
        save_data["items"],
        save_data["player_status"],
        save_data["player_name"],
        save_data.get("map_state", {})
    )


def run_map(map_state):
    """
    Runs the pygame world map where the player moves around.
    Displays town, monster sprites, and the player sprite.
    Movement uses arrow keys, and stepping onto a monster triggers combat.

    Parameters:
        map_state (dict): Persistent map containing player position,
                          town location, and monster list.

    Returns:
        tuple: (action, updated_map_state)
               action is "town", "fight", or "quit".
    """
    pygame.init()
    TILE = 32
    GRID = 10
    SCREEN = GRID * TILE
    screen = pygame.display.set_mode((SCREEN, SCREEN))
    pygame.display.set_caption("Adventure Map")
    clock = pygame.time.Clock()

    player_img = load_sprite("images/player.png", (0, 0, 255), TILE)
    goblin_img = load_sprite("images/goblin.png", (0, 255, 0), TILE)
    vulture_img = load_sprite("images/vulture.png", (255, 255, 0), TILE)
    orc_img = load_sprite("images/orc.png", (0, 120, 0), TILE)

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
    moves = 0
    action = None

    while running:
        screen.fill((0, 0, 0))

        for x in range(GRID):
            for y in range(GRID):
                pygame.draw.rect(screen, (50, 50, 50),
                                 pygame.Rect(x*TILE, y*TILE, TILE, TILE), 1)

        pygame.draw.circle(
            screen,
            (0, 255, 0),
            (town_pos[0]*TILE + TILE//2, town_pos[1]*TILE + TILE//2),
            TILE//2 - 2
        )

        for m in monsters:
            if m["alive"]:
                if m["name"] == "Goblin":
                    img = goblin_img
                elif m["name"] == "Vulture":
                    img = vulture_img
                else:
                    img = orc_img

                screen.blit(img, (m["pos"][0]*TILE, m["pos"][1]*TILE))

        screen.blit(player_img, (player_pos[0]*TILE, player_pos[1]*TILE))

        pygame.display.flip()
        clock.tick(10)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return "quit", map_state

            if event.type == pygame.KEYDOWN:
                moved = False
                if event.key == pygame.K_UP and player_pos[1] > 0:
                    player_pos[1] -= 1
                    moved = True
                elif event.key == pygame.K_DOWN and player_pos[1] < GRID-1:
                    player_pos[1] += 1
                    moved = True
                elif event.key == pygame.K_LEFT and player_pos[0] > 0:
                    player_pos[0] -= 1
                    moved = True
                elif event.key == pygame.K_RIGHT and player_pos[0] < GRID-1:
                    player_pos[0] += 1
                    moved = True

                if moved:
                    moves += 1

                    for m in monsters:
                        if m["alive"] and m["pos"] == player_pos:
                            action = "fight"
                            running = False
                            break

                    if player_pos == town_pos:
                        action = "town"
                        running = False

                    if moves % 3 == 0:
                        for m in monsters:
                            if m["alive"]:
                                dx, dy = random.choice([[0,1],[0,-1],[1,0],[-1,0]])
                                new_x = max(0, min(9, m["pos"][0]+dx))
                                new_y = max(0, min(9, m["pos"][1]+dy))
                                if [new_x,new_y] != player_pos and all([new_x,new_y] != mm["pos"] for mm in monsters if mm != m and mm["alive"]):
                                    m["pos"] = [new_x, new_y]

    map_state["player_pos"] = player_pos
    return action, map_state


def monster_fight(monster_dict, items):
    """
    Runs a text-based turn combat encounter.

    Parameters:
        monster_dict (dict): Stats of the enemy encountered.
        items (dict): Player inventory.

    Returns:
        int: Gold gained from killing the monster.
    """
    monster_hp = monster_dict["health"]
    player_status.setdefault("equipped_weapon", None)

    print(f"\nA wild {monster_dict['name']} appears!")
    print(monster_dict["description"])
    print(f"HP: {monster_hp}, Power: {monster_dict['power']}, Gold: {monster_dict['money']}")

    while monster_hp > 0 and player_status["hp"] > 0:
        print(f"\nYour HP: {player_status['hp']}   Monster HP: {monster_hp}")
        print("1) Attack")
        print("2) Use Item / Equip")
        print("3) Run")
        choice = input("> ").strip()

        if choice == "1":
            dmg = random.randint(5, 25)
            if random.random() < player_status["luck"]:
                dmg *= 2
                print("Critical hit!")
            if player_status["equipped_weapon"]:
                dmg += 10
            monster_hp -= dmg
            print(f"You deal {dmg} damage.")

            player_status["hp"] -= monster_dict["power"]
            print(f"The monster hits you for {monster_dict['power']}.")

        elif choice == "2":
            print("(item menu not altered)")
            return 0

        elif choice == "3":
            print("You escaped!")
            return 0

        if player_status["hp"] <= 0:
            print("You died!")
            return 0

    print(f"You defeated the {monster_dict['name']}!")
    return monster_dict["money"]


def town_menu(gold, items, player_name, map_state):
    """
    Handles the main town options: exploring, sleeping, shop, and quitting.

    Parameters:
        gold (int): Player gold.
        items (dict): Inventory.
        player_name (str): Player name.
        map_state (dict): Current map.

    Returns:
        tuple: (gold, items, player_name, updated_map_state, action)
               action "fight" triggers combat, otherwise stays in loop.
    """
    while True:
        print(f"\nYou are in town. HP: {player_status['hp']}, Gold: {gold}")
        print("1) Explore")
        print("2) Sleep (5 gold)")
        print("3) Shop")
        print("4) Save and Quit")
        print("5) Quit Without Saving")

        pick = input("> ").strip()

        if pick == "1":
            action, map_state = run_map(map_state)
            if action == "fight":
                return gold, items, player_name, map_state, "fight"
            if action == "quit":
                exit()

        elif pick == "2":
            if gold >= 5:
                gold -= 5
                player_status["hp"] = MAX_HP
                print("HP fully restored.")
            else:
                print("Not enough gold.")

        elif pick == "3":
            try:
                gold, items = gamefunctions.visit_shop(gold, items)
            except Exception:
                print("Shop error.")

        elif pick == "4":
            filename = input("Save file name: ")
            save_game(filename, gold, items, player_status, player_name, map_state)
            exit()

        elif pick == "5":
            exit()

        else:
            print("Invalid choice.")


def main():
    """
    Main game initializer. Loads or starts a new game and enters the town loop.

    Returns:
        None
    """
    print("Welcome to the Adventure Game!")
    pick = input("New game (N) or Load (L)? ").strip().upper()

    if pick == "L":
        filename = input("Filename: ")
        if os.path.exists(filename):
            gold, items, loaded_status, pname, map_state = load_game(filename)
            player_status.update(loaded_status)
            player_name = pname
        else:
            print("File not found. Starting new.")
            gold = random.randint(100, 300)
            items = {"potions": {}, "gear": []}
            player_status["hp"] = MAX_HP
            player_name = input("Name: ")
            map_state = {}
    else:
        gold = random.randint(100, 300)
        items = {"potions": {}, "gear": []}
        player_status["hp"] = MAX_HP
        player_name = input("Name: ")
        map_state = {}

    gamefunctions.print_welcome(player_name, 50)

    while True:
        gold, items, player_name, map_state, action = town_menu(
            gold, items, player_name, map_state
        )

        if action == "fight":
            fighting = [m for m in map_state["monsters"]
                        if m["alive"] and m["pos"] == map_state["player_pos"]]
            if fighting:
                monster = fighting[0]
                gained = monster_fight(monster, items)
                if player_status["hp"] <= 0:
                    break
                gold += gained
                monster["alive"] = False


if __name__ == "__main__":
    main()
