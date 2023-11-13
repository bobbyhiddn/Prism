from random import randint
import heapq
from itertools import combinations
import json  # For exporting the map in a JSON format

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
def draw_connection(x1, y1, x2, y2, grid):
    if abs(y2 - y1) > abs(x2 - x1):  # If rooms are more vertically aligned
        for i in range(min(y1, y2) + 3, max(y1, y2) - 2):  # Stop before entering the room
            if grid[i][x1] == " ":
                grid[i][x1] = "="  # Corridor path
        # Place doors at the boundary of the rooms
        if grid[min(y1, y2) + 2][x1] == "#":
            grid[min(y1, y2) + 2][x1] = "D"
        if grid[max(y1, y2) - 2][x1] == "#":
            grid[max(y1, y2) - 2][x1] = "D"
    else:  # If rooms are more horizontally aligned
        for j in range(min(x1, x2) + 3, max(x1, x2) - 2):  # Stop before entering the room
            if grid[y1][j] == " ":
                grid[y1][j] = "="  # Corridor path
        # Place doors at the boundary of the rooms
        if grid[y1][min(x1, x2) + 2] == "#":
            grid[y1][min(x1, x2) + 2] = "D"
        if grid[y1][max(x1, x2) - 2] == "#":
            grid[y1][max(x1, x2) - 2] = "D"

# Generate and return labyrinth map
def generate_labyrinth(grid_size=30):
    squares = []
    for _ in range(5):
        while True:
            x = randint(0, grid_size - 6)
            y = randint(0, grid_size - 6)
            new_square = (x, y)
            if all(not is_overlapping(new_square, existing_square) for existing_square in squares):
                squares.append(new_square)
                break

    grid = [[" " for _ in range(grid_size)] for _ in range(grid_size)]

    for x, y in squares:
        for i in range(y, y + 6):
            for j in range(x, x + 6):
                if i in {y, y + 5} or j in {x, x + 5}:
                    grid[i][j] = '#'
                else:
                    grid[i][j] = ' '

    edges = [(distance(square1, square2), square1, square2) for square1, square2 in pairs(squares)]
    heapq.heapify(edges)

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

    for (x1, y1), (x2, y2) in mst:
        mid_x1, mid_y1 = x1 + 3, y1 + 3
        mid_x2, mid_y2 = x2 + 3, y2 + 3

        closest_x1 = min(range(x1 + 2, x1 + 4), key=lambda x: abs(x - mid_x2))
        closest_y1 = min(range(y1 + 2, y1 + 4), key=lambda y: abs(y - mid_y2))
        closest_x2 = min(range(x2 + 2, x2 + 4), key=lambda x: abs(x - mid_x1))
        closest_y2 = min(range(y2 + 2, y2 + 4), key=lambda y: abs(y - mid_y1))

        if closest_y1 < closest_y2:
            draw_connection(closest_x1, closest_y1, closest_x1, closest_y2, grid)
            draw_connection(closest_x1, closest_y2 - 1, closest_x2, closest_y2 - 1, grid)
        else:
            draw_connection(closest_x1, closest_y1, closest_x1, closest_y2, grid)
            draw_connection(closest_x1, closest_y2 + 1, closest_x2, closest_y2 + 1, grid)

    return grid

# Function to export the generated labyrinth map to a plain text file
def export_map_to_file(map_data, file_name='labyrinth_map.txt'):
    with open(file_name, 'w') as file:
        for row in map_data:
            file.write("".join(row) + "\n")

# Function to generate and export the labyrinth map
def generate_and_export_labyrinth(grid_size=30):
    labyrinth_map = generate_labyrinth(grid_size)
    export_map_to_file(labyrinth_map)

# Generate and export labyrinth map when script is run
if __name__ == '__main__':
    generate_and_export_labyrinth()
