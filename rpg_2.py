import random
# Base class for all characters in the game
class Character:
    def __init__(self, name, health, power, bounty=0):
        # Initialize character attributes
        self.name = name
        self.health = health
        self.max_health = health
        self.power = power
        self.coins = 20  # New attribute with default value of 20
        self.bounty = bounty

    def attack(self, target):
        # Perform an attack on the target
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
        # Check if the character is still alive
        return self.health > 0

    def status(self):
        # Return a string describing the character's current status
        return f"{self.name} has {self.health} health, {self.power} power, and {self.coins} coins."

    def collect_bounty(self, defeated_enemy):
        self.coins += defeated_enemy.bounty
        print(f"{self.name} collects {defeated_enemy.bounty} coins bounty from {defeated_enemy.name}.")

    def flee(self):
        print(f"{self.name} flees from the battle. Goodbye!")
        return True

    def buy(self, item):
        if self.coins >= item.cost:
            self.coins -= item.cost
            print(f"{self.name} purchased {item.name} for {item.cost} coins.")
        else:
            print(f"{self.name} doesn't have enough coins to buy {item.name}.")

# Hero class, inherits from Character
class Hero(Character):
    def __init__(self, name="Hero"):
        # Initialize hero with default values
        super().__init__(name, health=10, power=5)

    def attack(self, target):
        # 20% chance to deal double damage
        if random.random() < 0.2:
            damage = self.power * 2
            print(f"{self.name} lands a critical hit!")
        else:
            damage = self.power
        target.receive_damage(damage)
        print(f"{self.name} does {damage} damage to {target.name}.")
        if not target.is_alive():
            print(f"{target.name} is dead.")
            self.collect_bounty(target)

    def flee(self):
        # Allow the hero to flee from battle
        print("You flee from the battle. Goodbye!")
        return True

    def buy(self, item):
        # Purchase an item from the virtual store
        if self.coins >= item.cost:
            self.coins -= item.cost
            print(f"{self.name} purchased {item.name} for {item.cost} coins.")
            # Here you can add logic to apply the item's effects
        else:
            print(f"{self.name} doesn't have enough coins to buy {item.name}.")


 # New Medic class
class Medic(Character):
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

# New Wizard class
class Wizard(Character):
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
    
# Goblin class, inherits from Character
class Goblin(Character):
    def __init__(self):
        # Initialize goblin with default values
        super().__init__(name="Goblin", health=6, power=2, bounty=5)

# New Shadow class
class Shadow(Character):
    def __init__(self):
        super().__init__("Shadow", health=1, power=1, bounty=6)

    def receive_damage(self, damage):
        if random.random() < 0.9:  # 90% chance to evade damage
            print(f"{self.name} evades the attack!")
        else:
            super().receive_damage(damage)

# New Zombie class
class Zombie(Character):
    def __init__(self, name="Zombie", health=5, power=1):
        super().__init__(name, health, power, bounty=0)  # Zombies don't give bounty

    def is_alive(self):
        return True  # Zombie always stays "alive"

    def receive_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            print(f"{self.name} is knocked down, but it's getting up again!")


# Game class to manage the game state and flow
class Game:
    def __init__(self):
        # Initialize the game with a hero and a goblin
        self.hero = self.choose_hero()
        self.enemies = [Goblin(), Shadow(), Zombie()]
        self.current_enemy = None

    def choose_hero(self):
        print("Choose your hero:")
        print("1. Hero (Balanced)")
        print("2. Medic (Can heal)")
        print("3. Wizard (Powerful spells, but low health)")
        while True:
            choice = input("> ")
            if choice == "1":
                return Hero(input("Enter hero name: "))
            elif choice == "2":
                return Medic(input("Enter medic name: "))
            elif choice == "3":
                return Wizard(input("Enter wizard name: "))
            else:
                print("Invalid choice. Please try again.")
    
    def get_new_enemy(self):
        self.current_enemy = random.choice(self.enemies)
        print(f"A {self.current_enemy} appears!")
    
    def display_status(self):
        # Display the current status of both characters
        print(self.hero.status())
        if self.current_enemy:
            print(self.current_enemy.status())
        print()

    def get_user_action(self):
        # Present options to the user and get their input
        print("What do you want to do?")
        print("1. Fight enemy")
        print("2. Do nothing")
        print("3. Flee")
        return input("> ")

    def play(self):
        # Main game loop
        while self.hero.is_alive():
            if not self.current_enemy or not self.current_enemy.is_alive():
                self.get_new_enemy()
            
            self.display_status()
            action = self.get_user_action()

            if action == "1":
                # Hero attacks goblin
                self.hero.attack(self.current_enemy)
                if self.current_enemy.is_alive():
                    # Goblin counterattacks if still alive
                    self.current_enemy.attack(self.hero)
            elif action == "2":
                # Hero does nothing, goblin attacks
                self.current_enemy(self.hero)
            elif action == "3":
                # Hero attempts to flee
                if self.hero.flee():
                    print("You've fled the battle. Game over.")
                    break
            else:
                # Handle invalid input
                print(f"Invalid input {action}")

        # Game over conditions
        if not self.hero.is_alive():
            print("You have been defeated. Game over.")
        

# Example Item class (for the virtual store)
class Item:
    def __init__(self, name, cost):
        self.name = name
        self.cost = cost

# Entry point of the program
if __name__ == "__main__":
    game = Game()
    game.play()