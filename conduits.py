import random

class Flame_Conduit_6:

    def __init__(self, charge=0):
        self.charge = charge
        self.spells = [self.ember, self.singe, self.flame_wall, self.inferno, self.blaze, self.firestorm]

    def ember(self):
        print('You throw an ember from your conduit, singeing your target.')

    def singe(self):
        print('You deal 1 damage to target. That target takes 1 damage at the beginning of the next turn.')

    def flame_wall(self):
        print('You summon a wall of flames from your conduit, burning your target and protecting you.')

    def inferno(self):
        print('You summon an inferno from your conduit, engulfing your target in scorching flames.')

    def blaze(self):
        print('You draw upon the pure essence of fire in your conduit, blasting your target with a powerful blaze but with recoil.')

    def firestorm(self):
        print('You unleash a firestorm from your conduit, raining down flames on all who oppose you.')

    def roll_spell(self):
        if self.charge == 1:
            return random.randint(1, 2)
        elif self.charge == 2:
            return random.randint(1, 4)
        elif self.charge == 3:
            return random.randint(1, 6)
        elif self.charge == 4:
            return random.randint(3, 6)
        elif self.charge == 5:
            return random.randint(4, 6)
        elif self.charge == 6:
            return random.randint(5, 6)
        elif self.charge >= 7:
            return 6
        else:
            return 0  # Return 0 if there is no charge

class Water_Conduit_4:

    def __init__(self, charge=0):
        self.charge = charge
        self.spells = [self.droplet, self.splash, self.water_wall, self.tsunami]

    def droplet(self):
        print('You throw a droplet from your conduit, splashing your target.')

    def splash(self):
        print('You deal 1 damage to target. That target takes 1 damage at the beginning of the next turn.')

    def water_wall(self):
        print('You summon a wall of water from your conduit, drowning your target and protecting you.')

    def tsunami(self):
        print('You summon a tsunami from your conduit, engulfing your target in a massive wave.')

    def roll_spell(self):
        if self.charge == 1:
            return random.randint(1, 2)
        elif self.charge == 2:
            return random.randint(1, 4)
        elif self.charge == 3:
            return random.randint(2, 4)
        elif self.charge == 4:
            return random.randint(3, 4)
        elif self.charge == 5:
            return 4
        else:
            return 0

class Water_Conduit_6:

    def __init__(self, charge=0):
        self.charge = charge
        self.spells = [self.droplet, self.splash, self.water_wall, self.tsunami, self.torrent, self.flood]

    def droplet(self):
        print('You throw a droplet from your conduit, splashing your target.')

    def splash(self):
        print('You deal 1 damage to target. That target takes 1 damage at the beginning of the next turn.')

    def water_wall(self):
        print('You summon a wall of water from your conduit, drowning your target and protecting you.')

    def tsunami(self):
        print('You summon a tsunami from your conduit, engulfing your target in a massive wave.')

    def torrent(self):
        print('You draw upon the pure essence of water in your conduit, blasting your target with a powerful torrent but with recoil.')

    def flood(self):
        print('You unleash a flood from your conduit, drowning all who oppose you.')

    def roll_spell(self):
        if self.charge == 1:
            return random.randint(1, 2)
        elif self.charge == 2:
            return random.randint(1, 4)
        elif self.charge == 3:
            return random.randint(1, 6)
        elif self.charge == 4:
            return random.randint(3, 6)
        elif self.charge == 5:
            return random.randint(4, 6)
        elif self.charge == 6:
            return random.randint(5, 6)
        elif self.charge >= 7:
            return 6
        else:
            return 0  # Return 0 if there is no charge

class Player:

    def __init__(self, mana=10):
        self.mana = mana
        self.conduits = []

    def add_conduit(self, conduit):
        self.conduits.append(conduit)

    def charge_conduit(self, conduit_index, amount):
        if amount <= self.mana:
            self.conduits[conduit_index].charge += amount
            self.mana -= amount
        else:
            print('Not enough mana')

def roll_dice(player, conduit_index, spell):
    conduit = player.conduits[conduit_index]
    if spell > 0:
        conduit.spells[spell-1]()
        conduit.charge = 0  # Reset the charge after the spell is cast
    else:
        print('No spell to cast. Increase the conduit charge.')

def select_conduit():
    conduits = [Flame_Conduit_6, Water_Conduit_6, Water_Conduit_4]  # Add new conduits to this list as you create them
    print("Select a conduit:")
    for i, conduit in enumerate(conduits, 1):
        print(f"{i}. {conduit.__name__}")
    selection = int(input("Enter the number of your selection: ")) - 1
    return conduits[selection]

def play_game():
    player1 = Player()

    while True:
        print('Your current mana is:', player1.mana)
        action = input('What would you like to do? Type "cast" or "quit": ')
        if action.lower() == 'quit':
            break
        elif action.lower() == 'cast':
            conduit_type = select_conduit()  # Player selects the conduit type
            player1_conduit = conduit_type()  # A new instance of the selected conduit is created
            player1.add_conduit(player1_conduit)

            charge = int(input('How much mana would you like to use to charge the conduit? '))
            player1.charge_conduit(-1, charge)  # Charging the last conduit in the list
            spell = player1.conduits[-1].roll_spell()  # Casting from the last conduit in the list
            print('You cast spell', spell)
            roll_dice(player1, -1, spell)

            player1.conduits.pop()  # Remove the last

play_game()