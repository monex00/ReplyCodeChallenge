from queue import PriorityQueue
import time

# (dx, dy)
base_directions = {
    "left" : (0, -1),
    "right" : (0, 1),
    "up" : (-1, 0),
    "down" : (1, 0),
}
directions = {
    # (pred, succ)
    "3": [("left", "right")],  # Da sinistra a destra
    "5": [("down", "right")],  # Da basso a destra
    "6": [("left", "down")],  # Da sinistra a basso
    "7": [("left", "right"), ("left", "down"), ("down", "right")],  # Da sinistra a destra, da sinistra a basso, da basso a destra
    "9": [("up", "right")],  # Da alto a destra
    "96": [("left", "down"), ("up", "right")],  # Da sinistra a basso, da alto a destra
    "A": [("left", "up")],  # Da sinistra a alto
    "A5": [("left", "up"), ("down", "right")],  # Da sinistra a alto, da basso a destra
    "B": [("left", "right"), ("left", "up"), ("up", "right")],  # Da sinistra a destra, da sinistra a alto, da alto a destra
    "C": [("up", "down")],  # Da alto a basso
    "C3": [("left", "right"), ("up", "down")],  # Da sinistra a destra, da alto a basso
    "D": [("up", "down"), ("up", "right"), ("down", "right")],  # Da alto a basso, da alto a destra, da basso a destra
    "E": [("left", "up"), ("left", "down"), ("up", "down")],  # Da sinistra a alto, da sinistra a basso, da alto a basso
    "F": [("left", "right"), ("up", "down"), ("left", "up"), ("left", "down"), ("up", "down"), ("up", "right")]  # Tutte le direzioni possibili
}

def read_input_file(filename):
    with open(filename, 'r') as file:
        w, h, g_n, s_m, t_l = map(int, file.readline().strip().split())
        
        # Inizializza le liste per i punti e le tiles
        golden_points = []
        silver_points = []
        grid = [[0 for _ in range(w)] for _ in range(h)]
        tiles = {}
        
        # Leggi i Punti Dorati
        for _ in range(g_n):
            x, y = map(int, file.readline().strip().split())
            golden_points.append((x, y))
            grid[y][x] = "G"
        
        # Leggi i Punti Argentati
        for _ in range(s_m):
            x, y, score = map(int, file.readline().strip().split())
            silver_points.append(((x, y), score))
            grid[y][x] = score
        
        # Leggi le informazioni sulle Tiles
        for _ in range(t_l):
            tile_id, cost, n = file.readline().strip().split()
            cost = int(cost)
            n = int(n)
            tiles[tile_id] = {'cost': cost, 'available': n}
    
    return w, h, golden_points, silver_points, tiles, grid

def get_neighbors(current, grid):
    neighbors = []
    x, y = current

    # for all the adjacent cell, try to place a tile
    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, 1), (1, -1), (-1, -1)]:
        for tile in tiles:
            for direction in directions[tile]:
                pred, succ = direction
                new_x = x + dx
                new_y = y + dy
                if x == new_x + base_directions[pred][0] and y == new_y + base_directions[pred][1]:
                    new_x_tile = new_x + base_directions[succ][0]
                    new_y_tile = new_y + base_directions[succ][1]
                    if 0 <= new_x < len(grid[0]) and 0 <= new_y < len(grid):
                        if grid[new_y][new_x] == 0:
                            neighbors.append((new_x, new_y, new_x_tile, new_y_tile, tile))
    return neighbors


def heuristic(a, b):
    # Manhattan distance
    (x1, y1), (x2, y2) = a, b
    return abs(x1 - x2) + abs(y1 - y2)

def a_star (start, goal, tiles, grid):
    frontier = PriorityQueue()
    frontier.put((0, start))
    came_from = {}
    cost_so_far = {}
    first_tile = list(tiles.keys())[0]
    came_from[start] = (None, None)
    cost_so_far[start] = 0

    while not frontier.empty():
        prio, current = frontier.get()
        if current == goal:
            print('Goal reached')
            break

        for next in get_neighbors(current, grid):
            new_x, new_y, new_x_tile, new_y_tile, tile = next
            print(new_x, new_y, new_x_tile, new_y_tile, tile)
            """ new_cost = cost_so_far[current] + tiles[tile]['cost']
            if (new_x, new_y) not in cost_so_far or new_cost < cost_so_far[(new_x, new_y)]:
                cost_so_far[(new_x, new_y)] = new_cost
                priority = new_cost + heuristic(goal, (new_x_tile, new_y_tile))
                frontier.put((priority, (new_x, new_y)))
                came_from[(new_x, new_y)] = (current, tile) """

    return came_from, cost_so_far

def reconstruct_path(came_from, start, goal):
    current = goal
    path = []
    while current != start:
        path.append(current)
        current, tile = came_from[current]
    path.append(start)
    path.reverse()
    return path

if __name__ == "__main__":
    input_filename = 'input.txt'
    w, h, golden_points, silver_points, tiles, grid = read_input_file(input_filename)
    tiles = {k: v for k, v in sorted(tiles.items(), key=lambda item: item[1]['cost'])}
    # print first tile

    start = (4, 2)
    end = (6, 6)
   
    came_from, cost_so_far = a_star(start, end, tiles, grid)
    """  path = reconstruct_path(came_from, start, end)
    print(path) """

    


 




 

    
    




