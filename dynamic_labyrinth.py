from random import randint
import heapq
from itertools import combinations

# Function to check if two squares overlap
def is_overlapping(square1, square2):
    x1, y1 = square1
    x2, y2 = square2
    return not (x1 + 5 < x2 or x2 + 5 < x1 or y1 + 5 < y2 or y2 + 5 < y1)

# Function to get all pairs of squares
def pairs(squares):
    return combinations(squares, 2)

# Function to calculate distance between two squares
def distance(square1, square2):
    x1, y1 = square1
    x2, y2 = square2
    return ((x2 - x1)**2 + (y2 - y1)**2)**0.5

# Function to draw connection
def draw_connection(x1, y1, x2, y2):
    if x1 == x2:  # North-South corridor
        for i in range(min(y1, y2), max(y1, y2) - 1):  # Stop before entering the room
            if grid[i][x1] == " " or grid[i][x1] == "=":
                grid[i][x1] = "="  # Corridor path
            elif grid[i][x1] == "#":
                grid[i][x1] = "D"  # Door
    elif y1 == y2:  # East-West corridor
        for j in range(min(x1, x2), max(x1, x2) - 1):  # Stop before entering the room
            if grid[y1][j] == " " or grid[y1][j] == "=":
                grid[y1][j] = "="  # Corridor path
            elif grid[y1][j] == "#":
                grid[y1][j] = "D"  # Door

# Grid size
grid_size = 30

# Generate random coords for 5 squares while avoiding overlap
squares = []
for _ in range(5):
    while True:
        x = randint(0, grid_size - 6)
        y = randint(0, grid_size - 6)
        new_square = (x, y)
        if all(not is_overlapping(new_square, existing_square) for existing_square in squares):
            squares.append(new_square)
            break

# Initialize empty grid
grid = [[" " for _ in range(grid_size)] for _ in range(grid_size)]

# Draw 5 squares at coords
for x, y in squares:
    for i in range(y, y + 6):
        for j in range(x, x + 6):
            if i in {y, y + 5} or j in {x, x + 5}:
                grid[i][j] = '#'
            else:
                grid[i][j] = ' '

# Spawn the player
player_square = squares[randint(0, len(squares) - 1)]  # Choosing a random square as starting point
player_position = (player_square[0] + 3, player_square[1] + 3)  # Placing the player in the center of the square
grid[player_position[1]][player_position[0]] = '0'

# Build a Minimum Spanning Tree to find the minimal set of connections between rooms
edges = [(distance(square1, square2), square1, square2) for square1, square2 in pairs(squares)]
heapq.heapify(edges)

# Use Union-Find to build the MST
parent = {square: square for square in squares}

def find(u):
    if u != parent[u]:
        parent[u] = find(parent[u])
    return parent[u]

mst = []
while edges:
    cost, u, v = heapq.heappop(edges)
    if find(u) != find(v):
        mst.append((u, v))
        parent[find(u)] = find(v)


# Draw the MST connections
for (x1, y1), (x2, y2) in mst:
    mid_x1, mid_y1 = x1 + 3, y1 + 3
    mid_x2, mid_y2 = x2 + 3, y2 + 3

    # Calculate the closest points excluding corners
    closest_x1 = min(range(x1 + 2, x1 + 4), key=lambda x: abs(x - mid_x2))
    closest_y1 = min(range(y1 + 2, y1 + 4), key=lambda y: abs(y - mid_y2))
    closest_x2 = min(range(x2 + 2, x2 + 4), key=lambda x: abs(x - mid_x1))
    closest_y2 = min(range(y2 + 2, y2 + 4), key=lambda y: abs(y - mid_y1))

    # Draw the corridors using the non-corner points
    if closest_y1 < closest_y2:
        draw_connection(closest_x1, closest_y1, closest_x1, closest_y2)
        draw_connection(closest_x1, closest_y2 - 1, closest_x2, closest_y2 - 1)
    else:
        draw_connection(closest_x1, closest_y1, closest_x1, closest_y2)
        draw_connection(closest_x1, closest_y2 + 1, closest_x2, closest_y2 + 1)

# Navigate the realm
# Modified navigation loop to track the player's path and prevent exiting the map
while True:
    for row in grid:
        print("".join(row))
    command = input("Command: ").lower()

    x, y = player_position

    def can_move_to(nx, ny):
        # Check if the next position is within the grid boundaries
        within_bounds = 0 <= nx < grid_size and 0 <= ny < grid_size
        # Check if the next position is a valid path (corridor, door, or player trail)
        is_valid_path = grid[ny][nx] in "=D. "
        return within_bounds and is_valid_path

    if command == 'n' and can_move_to(x, y - 1):  # North movement
        player_position = (x, y - 1)
    elif command == 's' and can_move_to(x, y + 1):  # South movement
        player_position = (x, y + 1)
    elif command == 'e' and can_move_to(x + 1, y):  # East movement
        player_position = (x + 1, y)
    elif command == 'w' and can_move_to(x - 1, y):  # West movement
        player_position = (x - 1, y)
    else:
        print("Invalid command or blocked path")
        continue

    # Update the grid with the player's new position
    grid[y][x] = '.'  # Mark the trail of the player
    new_x, new_y = player_position
    grid[new_y][new_x] = '0'  # Mark new position
