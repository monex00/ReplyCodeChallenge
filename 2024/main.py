from queue import PriorityQueue
import time
# (su/giu, destra/sinistra)
directions = {
    "3": [(0, 1)],  # Da sinistra a destra
    "5": [(-1, 1)],  # Da basso a destra
    "6": [(1, 1)],  # Da sinistra a basso
    "7": [(0, 1), (1, 0), (1, 1)],  # Da sinistra a destra, da sinistra a basso, da basso a destra
    "9": [(-1, 1)],  # Da alto a destra
    "96": [(1, 0), (-1, 1)],  # Da sinistra a basso, da alto a destra
    "A": [(0, -1)],  # Da sinistra a alto
    "A5": [(0, -1), (1, 1)],  # Da sinistra a alto, da basso a destra
    "B": [(0, 1), (0, -1), (-1, 1)],  # Da sinistra a destra, da sinistra a alto, da alto a destra
    "C": [(1, 0), (-1, 0)],  # Da alto a basso
    "C3": [(0, 1), (1, 0), (-1, 0)],  # Da sinistra a destra, da alto a basso
    "D": [(1, 0), (-1, 0), (-1, 1)],  # Da alto a basso, da alto a destra, da basso a destra
    "E": [(0, -1), (1, 0), (-1, 0)],  # Da sinistra a alto, da sinistra a basso, da alto a basso
    "F": [(0, 1), (1, 0), (0, -1), (-1, 0), (-1, 1), (1, 1)]  # Tutte le direzioni possibili
}

# some tiles can only connect to some other tiles
# for example, tile 3 can only connect to tile 5
# this is a dictionary that maps a tile to a list of tiles it can connect to
allowed_connections = {
    "3": ["3", "6", "7", "A", "B", "E", "F"], # "96", "A5",
    "5": ["6", "7", "A", "B", "E", "F"], # "96",  "A5",
    "6": ["9", "B", "A", "C", "D", "E", "F"], # "96", "A5",
    "7": ["7", "3", "6", "A", "B", "C", "E", "F"], # "96", "A" "A5"
    "9": ["3", "6", "7", "B", "E", "F"], # "96", "A", "A5"
    "96": ["3", "5", "6", "7", "9", "A", "A5", "B", "C", "D", "E", "F"],
    "A": ["5", "7", "C", "D", "E", "F"], # "96", "A5",
    "A5": ["3", "5", "6", "7", "9", "96", "A", "B", "C", "D", "E", "F"],
    "B": ["3", "5", "6", "7", "9", "96", "A", "A5", "C", "D", "E", "F"],
    "C": ["3", "5", "6", "7", "9", "96", "A", "A5", "B", "D", "E", "F"],
    "D": ["3", "5", "6", "7", "9", "96", "A", "A5", "B", "C", "E", "F"],
    "E": ["3", "5", "6", "7", "9", "96", "A", "A5", "B", "C", "D", "F"],
    "F": ["3", "5", "6", "7", "9", "96", "A", "A5", "B", "C", "D", "E"]
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


def heuristic(a, b):
    # Manhattan distance
    (x1, y1), (x2, y2) = a, b
    return abs(x1 - x2) + abs(y1 - y2)

def get_neighbors(point, grid, previus_tile):
    x, y = point
    neighbors = []

    for tile in tiles:
        if previus_tile is not None and tile not in allowed_connections[previus_tile]:
            continue
        for direction in directions[tile]:
            dx, dy = direction
            new_x = x + dx
            new_y = y + dy
            if new_x >= 0 and new_x < len(grid[0]) and new_y >= 0 and new_y < len(grid):
                neighbors.append((new_x, new_y, tile))
    """     for direction in directions[tile]:
        dx, dy = direction
        new_x = x + dx
        new_y = y + dy
        if new_x >= 0 and new_x < len(grid[0]) and new_y >= 0 and new_y < len(grid):
            if previus_tile is not None:
                if tile in allowed_connections[previus_tile]:
                    neighbors.append((new_x, new_y))
            else:
                neighbors.append((new_x, new_y)) """

    return neighbors

def a_star_search(start, goal, tiles, grid):
    frontier = PriorityQueue()
    frontier.put((0, start))
    # print(frontier.queue)
    print()
    came_from = {}
    cost_so_far = {}
    came_from[start] = (None, None)
    cost_so_far[start] = 0

    while not frontier.empty():
         # print(frontier.queue)

        prio, current = frontier.get()
        # print("get", current)

        if current == goal:
            print('Goal reached')
            break
            
        # previus_tile = came_from[current][1]
        for (x, y, tile) in get_neighbors(current, grid, came_from[current][1]):
            new_cost = cost_so_far[current] # + tiles[tile]['cost']
            if (x, y) not in cost_so_far or new_cost < cost_so_far[(x, y)]:
                cost_so_far[(x, y)] = new_cost
                priority = new_cost + heuristic(goal, (x, y))
                frontier.put((priority, (x, y)))
                # print("put", (x, y), new_cost, heuristic(goal, (x, y)), priority)
                # print(frontier.queue)

                came_from[(x, y)] = (current, tile)
                grid[current[0]][current[1]] = tile
 
                  
    return came_from, cost_so_far

def get_path(start, goal, came_from):
    current = goal
    path = []
    while current != start:
        path.append((current, came_from[current][1])) # aggiungi la tile
        current = came_from[current][0]
    path.append((start, None))
    path.reverse()
    return path

def get_tile_path(path):
    return [tile for point, tile in path]


if __name__ == "__main__":

    '''
    types :
    tiles = {
        'A': {'cost': 1, 'available': 2},
        'B': {'cost': 2, 'available': 3},
        'C': {'cost': 3, 'available': 1}
    }
    golden_points = [(1, 2), (3, 4), (5, 6)]
    silver_points = [
        ((1, 2), 10),
        ((3, 4), 20),
        ((5, 6), 30)
    ]
    '''
    # Esempio di utilizzo
    input_filename = 'input.txt'  # Sostituisci con il percorso effettivo del tuo file di input
    w, h, golden_points, silver_points, tiles, grid = read_input_file(input_filename)

    # order tiles by cost
    tiles = {k: v for k, v in sorted(tiles.items(), key=lambda item: item[1]['cost'])}
    
    start = (4, 2)
    end = (6, 6)
   
    came_from, cost_so_far = a_star_search(start, end, tiles, grid)
   
    print(get_path(start, end, came_from))
    print(get_tile_path(get_path(start, end, came_from)))
    for row in grid:
        print(row)
    """ que = PriorityQueue()
    que.put((6, (1, 2)))
    que.put((8, (3, 4)))
    que.put((4, (5, 6)))
    print(que.queue)
    print(que.get())
    print(que.queue)
     """


    


 




 

    
    




