import random
import pygame

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


# ---------------------------
# New Pygame Map Function
# ---------------------------

def run_map(map_state=None):
    """
    Launch a 10x10 grid map where the player moves with arrow keys.
    Green tile = town, red tile = monster.
    Returns a tuple: (result:str, updated map_state:dict)
    """
    pygame.init()
    
    TILE_SIZE = 32
    GRID_SIZE = 10
    SCREEN_SIZE = GRID_SIZE * TILE_SIZE
    screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
    pygame.display.set_caption("Map Exploration")
    
    clock = pygame.time.Clock()

    # Initialize map state if not passed
    if map_state is None:
        map_state = {
            "player_pos": [0, 0],
            "town_pos": [0, 0],
            "monster_pos": [random.randint(1, 9), random.randint(0, 9)],
            "monster_alive": True
        }

    player_pos = map_state["player_pos"]
    town_pos = map_state["town_pos"]
    monster_pos = map_state["monster_pos"]
    monster_alive = map_state["monster_alive"]

    running = True
    result = None

    while running:
        screen.fill((0, 0, 0))  # black background

        # Draw grid
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                rect = pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE)
                pygame.draw.rect(screen, (50,50,50), rect, 1)

        # Draw town (green)
        pygame.draw.circle(screen, (0, 255, 0),
                           (town_pos[0]*TILE_SIZE + TILE_SIZE//2, town_pos[1]*TILE_SIZE + TILE_SIZE//2), TILE_SIZE//2 - 2)

        # Draw monster (red) if alive
        if monster_alive:
            pygame.draw.circle(screen, (255, 0, 0),
                               (monster_pos[0]*TILE_SIZE + TILE_SIZE//2, monster_pos[1]*TILE_SIZE + TILE_SIZE//2), TILE_SIZE//2 - 2)

        # Draw player (blue)
        pygame.draw.rect(screen, (0, 0, 255), pygame.Rect(player_pos[0]*TILE_SIZE, player_pos[1]*TILE_SIZE, TILE_SIZE, TILE_SIZE))

        pygame.display.flip()
        clock.tick(10)  # 10 FPS

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return "quit", map_state

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and player_pos[1] > 0:
                    player_pos[1] -= 1
                elif event.key == pygame.K_DOWN and player_pos[1] < GRID_SIZE-1:
                    player_pos[1] += 1
                elif event.key == pygame.K_LEFT and player_pos[0] > 0:
                    player_pos[0] -= 1
                elif event.key == pygame.K_RIGHT and player_pos[0] < GRID_SIZE-1:
                    player_pos[0] += 1

                # Check for stepping on town
                if player_pos == town_pos:
                    running = False
                    result = "town"

                # Check for stepping on monster
                if monster_alive and player_pos == monster_pos:
                    running = False
                    result = "monster"

    # Save updated state
    map_state["player_pos"] = player_pos
    map_state["monster_alive"] = monster_alive
    return result, map_state
