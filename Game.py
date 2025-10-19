import gamefunctions
import random

def main():
    # Step 1: Welcome the player
    player_name = input("Enter your name, adventurer: ")
    gamefunctions.print_welcome(player_name, 50)

    print("\nWelcome to the potion shop!\n")

    # Step 2: Show shop menu
    potions = [
        ("Health Potion", (40, 60)),
        ("MP Potion", (30, 50)),
        ("Strength Potion", (100, 130)),
        ("Defense Potion", (90, 120)),
        ("Cloaking Potion", (80, 100)),
        ("Speed Potion", (70, 90))
    ]

    item1, item2 = random.sample(potions, 2)
    item1_price = round(random.uniform(*item1[1]), 2)
    item2_price = round(random.uniform(*item2[1]), 2)

    gamefunctions.print_shop_menu(item1[0], item1_price, item2[0], item2_price)

    # Step 3: Let player try to purchase an item
    gold = random.randint(100, 300)
    print(f"\nYou have {gold} gold.")

    choice = input(f"Which item do you want to buy? ({item1[0]} or {item2[0]}): ").strip().lower()
    quantity = int(input("How many do you want to buy? "))

    # Determine price of selected item
    if choice == item1[0].lower():
        price = int(item1_price)
    elif choice == item2[0].lower():
        price = int(item2_price)
    else:
        print("That item isn't in the shop!")
        return

    bought, remaining = gamefunctions.purchase_item(price, gold, quantity)
    print(f"\nYou bought {bought} potion(s).")
    print(f"Gold remaining: {remaining}")

    # Step 4: Encounter a monster
    print("\nAs you leave the shop, danger finds you...")
    monster = gamefunctions.new_random_monster()
    print(f"\n⚔️  A wild {monster['name']} appears!")
    print(monster['description'])
    print(f"Health: {monster['health']}, Power: {monster['power']}, Gold: {monster['money']}")

if __name__ == "__main__":
    main()
