import random

class Character:
    def __init__(self, name, health, power, bounty=0):
        self.name = name
        self.health = health
        self.max_health = health
        self.power = power
        self.coins = 20
        self.bounty = bounty

    def attack(self, target):
        damage = self.power
        target.receive_damage(damage)
        print(f"{self.name} does {damage} damage to {target.name}.")
        if not target.is_alive():
            print(f"{target.name} is dead.")
            self.collect_bounty(target)
    
    def receive_damage(self, damage):
        self.health -= damage
        self.health = max(0, self.health)

    def is_alive(self):
        return self.health > 0

    def status(self):
        return f"{self.name} has {self.health}/{self.max_health} health, {self.power} power, and {self.coins} coins."

    def collect_bounty(self, defeated_enemy):
        self.coins += defeated_enemy.bounty
        print(f"{self.name} collects {defeated_enemy.bounty} coins bounty from {defeated_enemy.name}.")

    def flee(self):
        print(f"{self.name} flees from the battle. Goodbye!")
        return True

class Hero(Character):
    def __init__(self, name, health, power):
        super().__init__(name, health, power)
        self.inventory = []

    def buy(self, item):
        if self.coins >= item.cost:
            self.coins -= item.cost
            self.inventory.append(item)
            print(f"{self.name} bought {item.name} for {item.cost} coins.")
        else:
            print(f"{self.name} doesn't have enough coins to buy {item.name}.")

    def use_item(self, item_index):
        if 0 <= item_index < len(self.inventory):
            item = self.inventory.pop(item_index)
            item.apply(self)
        else:
            print("Invalid item index.")

class Warrior(Hero):
    def __init__(self, name="Warrior"):
        super().__init__(name, health=10, power=5)

    def attack(self, target):
        if random.random() < 0.2:  # 20% chance for double damage
            damage = self.power * 2
            print(f"{self.name} lands a critical hit!")
        else:
            damage = self.power
        target.receive_damage(damage)
        print(f"{self.name} does {damage} damage to {target.name}.")
        if not target.is_alive():
            print(f"{target.name} is dead.")
            self.collect_bounty(target)

class Wizard(Hero):
    def __init__(self, name="Wizard"):
        super().__init__(name, health=8, power=1)
        self.mana = 10
        self.max_mana = 10

    def attack(self, target):
        if self.mana >= 5:
            damage = self.power * 3
            self.mana -= 5
            print(f"{self.name} casts a powerful spell!")
        else:
            damage = self.power
            print(f"{self.name} is out of mana and attacks normally.")
        target.receive_damage(damage)
        print(f"{self.name} does {damage} damage to {target.name}.")
        if not target.is_alive():
            print(f"{target.name} is dead.")
            self.collect_bounty(target)
        self.restore_mana()

    def restore_mana(self):
        mana_restored = random.randint(1, 3)
        self.mana = min(self.max_mana, self.mana + mana_restored)
        print(f"{self.name} restores {mana_restored} mana.")

    def status(self):
        return f"{super().status()} Mana: {self.mana}/{self.max_mana}."

class Medic(Hero):
    def __init__(self, name="Medic"):
        super().__init__(name, health=10, power=3)
        self.heal_chance = 0.2
        self.heal_amount = 2

    def attack(self, target):
        super().attack(target)
        if random.random() < self.heal_chance:
            self.heal()

    def heal(self):
        if self.health < self.max_health:
            self.health = min(self.max_health, self.health + self.heal_amount)
            print(f"{self.name} heals for {self.heal_amount} health!")

class Enemy(Character):
    pass

class Goblin(Enemy):
    def __init__(self):
        super().__init__(name="Goblin", health=6, power=2, bounty=5)

class Shadow(Enemy):
    def __init__(self):
        super().__init__("Shadow", health=1, power=1, bounty=6)

    def receive_damage(self, damage):
        if random.random() < 0.9:  # 90% chance to evade damage
            print(f"{self.name} evades the attack!")
        else:
            super().receive_damage(damage)

class Zombie(Enemy):
    def __init__(self):
        super().__init__("Zombie", health=5, power=1, bounty=0)

    def is_alive(self):
        return True  # Zombie always stays "alive"

    def receive_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            print(f"{self.name} is knocked down, but it's getting up again!")

class Item:
    def __init__(self, name, cost):
        self.name = name
        self.cost = cost

    def apply(self, character):
        pass

class Tonic(Item):
    def __init__(self):
        super().__init__("Tonic", 5)

    def apply(self, character):
        healing = 2
        character.health = min(character.max_health, character.health + healing)
        print(f"{character.name} used a Tonic and gained {healing} health!")

class Sword(Item):
    def __init__(self):
        super().__init__("Sword", 10)

    def apply(self, character):
        character.power += 2
        print(f"{character.name} equipped a Sword and gained 2 power!")

class Store:
    def __init__(self):
        self.items = [Tonic(), Sword()]

    def do_shopping(self, hero):
        while True:
            print(f"\nWelcome to the store, {hero.name}!")
            print(f"You have {hero.coins} coins.")
            print("Available items:")
            for i, item in enumerate(self.items, 1):
                print(f"{i}. {item.name} (Cost: {item.cost} coins)")
            print("0. Exit store")

            choice = input("Enter the number of the item you want to buy (or 0 to exit): ")
            if choice == "0":
                print("Thank you for visiting!")
                break
            try:
                item_index = int(choice) - 1
                if 0 <= item_index < len(self.items):
                    item = self.items[item_index]
                    hero.buy(item)
                else:
                    print("Invalid item number. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")

class Game:
    def __init__(self):
        self.hero = self.choose_hero()
        self.enemies = [Goblin(), Shadow(), Zombie()]
        self.current_enemy = None
        self.store = Store()

    def choose_hero(self):
        while True:
            print("\nChoose your hero:")
            print("1. Warrior")
            print("2. Wizard")
            print("3. Medic")
            choice = input("Enter the number of your chosen hero: ")
            if choice == "1":
                return Warrior()
            elif choice == "2":
                return Wizard()
            elif choice == "3":
                return Medic()
            else:
                print("Invalid choice. Please try again.")

    def select_enemy(self):
        if self.enemies:
            self.current_enemy = random.choice(self.enemies)
        else:
            self.current_enemy = None

    def display_status(self):
        print("\n" + "=" * 30)
        print(self.hero.status())
        print(f"Inventory: {[item.name for item in self.hero.inventory]}")
        if self.current_enemy:
            print(self.current_enemy.status())
        print("=" * 30 + "\n")

    def get_user_action(self):
        print("What do you want to do?")
        print("1. Fight enemy")
        print("2. Do nothing")
        print("3. Use item")
        print("4. Go to store")
        print("5. Flee")
        return input("> ")

    def play(self):
        self.select_enemy()
        while self.hero.is_alive() and (self.current_enemy or self.enemies):
            self.display_status()
            action = self.get_user_action()

            if action == "1":
                if self.current_enemy:
                    self.hero.attack(self.current_enemy)
                    if self.current_enemy.is_alive():
                        self.current_enemy.attack(self.hero)
                    else:
                        if not isinstance(self.current_enemy, Zombie):
                            self.enemies.remove(self.current_enemy)
                        self.select_enemy()
                else:
                    print("No enemy to fight!")
            elif action == "2":
                if self.current_enemy:
                    self.current_enemy.attack(self.hero)
                else:
                    print("No enemy to attack you!")
            elif action == "3":
                if self.hero.inventory:
                    print("Your inventory:")
                    for i, item in enumerate(self.hero.inventory):
                        print(f"{i + 1}. {item.name}")
                    item_choice = input("Enter the number of the item you want to use: ")
                    try:
                        item_index = int(item_choice) - 1
                        self.hero.use_item(item_index)
                    except ValueError:
                        print("Invalid input. Please enter a number.")
                else:
                    print("Your inventory is empty.")
            elif action == "4":
                self.store.do_shopping(self.hero)
            elif action == "5":
                if self.hero.flee():
                    break
            else:
                print(f"Invalid input {action}")

        if not self.hero.is_alive():
            print("You have been defeated. Game over.")
        elif not self.enemies:
            print("You have defeated all enemies. Victory!")

if __name__ == "__main__":
    game = Game()
    game.play()