# Base class for all characters in the game
class Character:
    def __init__(self, name, health, power):
        # Initialize character attributes
        self.name = name
        self.health = health
        self.power = power

    def attack(self, target):
        # Perform an attack on the target
        damage = self.power
        target.health -= damage
        print(f"{self.name} does {damage} damage to {target.name}.")
        if target.health <= 0:
            print(f"{target.name} is dead.")

    def is_alive(self):
        # Check if the character is still alive
        return self.health > 0

    def status(self):
        # Return a string describing the character's current status
        return f"{self.name} has {self.health} health and {self.power} power."
    

# Hero class, inherits from Character
class Hero(Character):
    def __init__(self, name="Hero", health=10, power=5):
        # Initialize hero with default values
        super().__init__(name, health, power)

    def flee(self):
        # Allow the hero to flee from battle
        print("You flee from the battle. Make haste!")
        return True

# Goblin class, inherits from Character
class Goblin(Character):
    def __init__(self, name="Goblin", health=6, power=2):
        # Initialize goblin with default values
        super().__init__(name, health, power)

# Game class to manage the game state and flow
class Game:
    def __init__(self):
        # Initialize the game with a hero and a goblin
        self.hero = Hero()
        self.goblin = Goblin()

    def display_status(self):
        # Display the current status of both characters
        print(self.hero.status())
        print(self.goblin.status())
        print()

    def get_user_action(self):
        # Present options to the user and get their input
        print("What do you want to do?")
        print("1. Fight goblin")
        print("2. Do nothing")
        print("3. Flee")
        return input("> ")

    def play(self):
        # Main game loop
        while self.hero.is_alive() and self.goblin.is_alive():
            self.display_status()
            action = self.get_user_action()

            if action == "1":
                # Hero attacks goblin
                self.hero.attack(self.goblin)
                if self.goblin.is_alive():
                    # Goblin counterattacks if still alive
                    self.goblin.attack(self.hero)
            elif action == "2":
                # Hero does nothing, goblin attacks
                self.goblin.attack(self.hero)
            elif action == "3":
                # Hero attempts to flee
                if self.hero.flee():
                    break
            else:
                # Handle invalid input
                print(f"Invalid input {action}")

        # Game over conditions
        if not self.hero.is_alive():
            print("You have been defeated. Game over.")
        elif not self.goblin.is_alive():
            print("You have defeated the goblin. Victory!")

# Entry point of the program
if __name__ == "__main__":
    game = Game()
    game.play()