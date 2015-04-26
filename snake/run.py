#!/bin/python
import pexpect
import sys

sys.path.append('../viewer')
import mazes
import snapshot

n_players = 4

print("Assuming you have more than " + str(n_players) + " cores..")

player_bins = ["python example_player.py" for x in range(n_players)]
max_mem = 100000                                        # memory beschikbaar voor spelers in kb
core_ids = ["0x"+str(x) for x in range(n_players)]      # namen van cores
                                                        # start restricted processen voor spelers
players = [pexpect.spawn("./timeout -m "+str(max_mem)+" taskset "+core_ids[x]+" "+player_bins[x]) for x in range(n_players)]


width = 40
height = 20
n_food_init = 10

# maze stores players, food, walls and open space
maze = mazes.generate_maze(width,height)


# Store state in snapshot
state = snapshot.Snapshot()
state.width = width
state.height = height
state.content = maze
state.names = player_bins
state.scores = [  0 for x in range(n_players)]
state.status = [ '' for x in range(n_players)]

# TODO: make beginning coordinates symmetric instead of random
state.snakes = [ [mazes.get_empty_cell(maze, width, height, str(x))] for x in range(n_players)]
state.food = [mazes.get_empty_cell(maze, width, height, 'x') for x in range(n_food_init)]


# Initialize players
for player_i in range(n_players):
    print("Initializing player "+str(player_i))
    p = players[player_i]

    p.sendline(str(height))
    p.sendline(str(width))
    for line in state.content:
        p.sendline("".join(line))
    p.sendline(str(n_players))
    for i in range(n_players):
        p.sendline(str(state.snakes[i][0][0])+" "+str(state.snakes[i][0][1]))
    p.sendline(str(player_i))

direction_chars = ['u',    'd',    'l',    'r']
direction_x     = {'u': 0, 'd': 0, 'l':-1, 'r': 1}
direction_y     = {'u':-1, 'd': 1, 'l': 0, 'r': 0}

n_food_iter = int(n_players/4)

max_timesteps = 10
old_moves = ""
spawn_food = []

# The time step
for timestep in range(max_timesteps):
    mazes.show_maze(maze)
    # We will obtain new_moves after passing old_moves to the players

    # TODO: make symmetric, make sure amounts are right (will crash when no space left!)
    new_moves = ""

    for player_i in range(n_players): 
        if state.status[player_i] == 'dead':
            new_moves += 'x'
            continue

        p = players[player_i]

        # Send moves + new food coordinates
        if len(old_moves) > 0:
            p.sendline(old_moves)
            p.sendline(str(len(spawn_food)))
            for food in spawn_food:
                p.sendline(str(food[0]) + " " + str(food[1]))
        
        # Read moves
        direction_index = p.expect(direction_chars)
        # TODO: check for timeout!
        new_moves += direction_chars[direction_index]

    old_moves = new_moves
    spawn_food = [mazes.get_empty_cell(maze, width, height, 'x') for x in range(n_food_iter)]
    

    # Update snapshot

    heads = []  # lists of positions about to be added or removed to snakes
    tails = []
    for player_i in range(n_players):   # Get all old/new coordinates
        if state.status[player_i] == 'dead':
            continue
        head_x = (state.snakes[player_i][-1][0] +
                     direction_x[new_moves[player_i]] + 1 + width) % width
        head_y = (state.snakes[player_i][-1][1] +
                     direction_y[new_moves[player_i]] + 1 + height) % height
        
        next_pos = maze[head_y][head_x]
        heads.append([head_y, head_x])
        if next_pos == 'x':
            tails.append("None") # A snake that eats has no "tail"
        else:
            tails.append(state.snakes[player_i][0])
    
    for player_i in range(n_players):
        if state.status[player_i] == 'dead':
            continue

        next_pos = maze[head_y][head_x]
    
        # First we determine if we can move a snake without dying
        valid_move = True 
        if next_pos == '#':
            valid_move = False
        elif next_pos == '.' or next_pos == 'x':
            if heads.count(heads[player_i]) > 1:    # More than one snake moves here
                valid_move = False
        else: # It must be another snake
            player_other = int(next_pos)
            valid_move = False
            if tails[player_other] == heads[player_i]: # The other snake moves away
                valid_move = True
                if heads.count(heads[player_i]) > 1: # More than one snake moves here
                    valid_move = False
            
        if valid_move: # The snake can move forward!
            state.snakes[player_i].append([head_x,head_y])
            maze[head_y][head_x] = str(player_i)
            if next_pos != 'x': # If no food is eaten, we must remove the tail
                tail=state.snakes[player_i].pop(0)
                maze[tail[1]][tail[0]] = '.'
        else: # We must have collided (note that you can collide with a dead snake)
            state.status[player_i] = 'dead'
            players[player_i].sendline("quit") # Gently stop the process
            print("Player "+str(player_i)+" died!")
            # TODO: remove body of dead snake?
            # TODO: force program to exit as well?

        #TODO: stop iteration if all players are dead or if game stagnates
        #TODO: scoring

