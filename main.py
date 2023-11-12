# ## Concept 

# So. I need to make a class for a room. I need to make a class for a player. A room can have up to 4 doors. 

# We start by generating a room and placing the player in it. Place a door on one of the 4 sides of the room and represent it as a variable with a value 1-4. 1-4 represent the cardinal directions(north, south, east, west). Player moves through the door, and a variable Last_Door is populated with the opposite directional value of the direction it was in in the last room. If you entered a north door, the next room has a south door. The next room then spawns 1-3 new doors in all but the LastDoor value. Continue until we have a map. 

# ## Pseudocode

# 1. Generate a room with a player in it.
# 2. Generate a door on one of the 4 sides of the room.
# 3. Player moves through the door, and a variable Last_Door is populated with the opposite directional value of the direction it was in in the last room.
# 4. If you entered a north door, the next room has a south door.
# 5. The next room then spawns 1-3 new doors in all but the LastDoor value.

# ## Code

import random

class Room:
    def __init__(self, name, description, north, south, east, west):
        self.name = name
        self.description = description
        self.north = north
        self.south = south
        self.east = east
        self.west = west

    def move(self, direction):
        global current_node
        current_node = globals()[getattr(self, direction)]

# Player Class

class Player:
    def __init__(self, name, current_node):
        self.name = name
        self.current_node = current_node

    def move(self, new_node):
        self.current_node = new_node
