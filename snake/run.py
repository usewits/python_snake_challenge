#!/bin/python
import pexpect
import sys

sys.path.append('../viewer')
import mazes
import snapshot

import os #TMP

n_players = 4

print("Assuming you have more than " + str(n_players) + " cores..")

player_bins = ["python clever_example_player2.py" for x in range(n_players)]
#player_bins[0] = "python clever_example_player_debug.py"#REMOVE ME
max_mem = 100000                                        # memory beschikbaar voor spelers in kb
core_ids = [hex(1<<x) for x in range(n_players)]      # namen van cores
print(core_ids)
                                                        # start restricted processen voor spelers
players = [pexpect.spawnu("./timeout -m "+str(max_mem)+" taskset "+core_ids[x]+" "+player_bins[x]) for x in range(n_players)]
player_logs_send = [open("logs/in"+str(i)+".txt", 'w') for i in range(n_players)]
player_logs_read = [open("logs/out"+str(i)+".txt", 'w') for i in range(n_players)]
game_log = open("logs/game.txt", 'w')

for i in range(n_players):
    players[i].logfile_send = player_logs_send[i]
    players[i].logfile_read = player_logs_read[i]


width = 40
height = 20

# maze stores players, food, walls and open space
maze = mazes.generate_maze(width,height,0.1)


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
state.food = []

os.remove("player0")
debug_out = open("player0","w")

# Initialize players
for player_i in range(n_players):
    #print("Initializing player "+str(player_i))
    p = players[player_i]
    
    init_string = ""
    init_string += str(height) + "\n"
    init_string += str(width) + "\n"
    lines = ["".join(line) for line in state.content]
    init_string += "\n".join(lines) + "\n"
    init_string += str(n_players) + "\n"
    for i in range(n_players):
        init_string += str(state.snakes[i][0][0])+" "+str(state.snakes[i][0][1]) + "\n"
    init_string += str(player_i)
    if player_i == 0:
        debug_out.write(init_string+"\n")
    p.sendline(str(init_string))

direction_chars = ['u',    'd',    'l',    'r']
direction_x     = {'u': 0, 'd': 0, 'l':-1, 'r': 1}
direction_y     = {'u':-1, 'd': 1, 'l': 0, 'r': 0}

n_food_iter = int(n_players/4)

max_timesteps = 500
old_moves = ""
spawn_food = []

# The time step
for timestep in range(max_timesteps):
    game_log.write("TIMESTEP "+str(timestep)+"\n")
    mazes.show_maze(maze, game_log)
    print("\nTimestep "+str(timestep))
    mazes.show_maze(maze)
    game_log.write("/TIMESTEP "+str(timestep)+"\n")
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
            update_string = ""
            update_string += old_moves + "\n"
            update_string += str(len(spawn_food)) + "\n"
            update_string += "\n".join([str(food[0]) + " " + str(food[1]) for food in spawn_food])
            if player_i == 0:
                debug_out.write(update_string+"\n")
            #print(update_string)
            p.sendline(update_string)
        
        # Read moves
        try:
            p.expect("move")
            direction_index = p.expect(direction_chars)
        except:
            game_log.write("Player "+str(player_i)+"'s AI crashed!\n")
            game_log.write("As a result, player "+str(player_i)+" has been declared dead\n")
            state.status[player_i] = 'dead'
            new_moves += 'x'
            continue
        #print("player "+str(player_i) + " moves "+str(direction_index) + " aka " + direction_chars[direction_index]) #DEBUG
        # TODO: check for timeout!
        new_moves += direction_chars[direction_index]

    old_moves = new_moves
    spawn_food = [mazes.get_empty_cell(maze, width, height, 'x') for x in range(n_food_iter)]
    
    game_log.write("Moves to be executed: " + new_moves + "\n")

    # Update snapshot

    heads = []  # lists of positions about to be added or removed to snakes
    tails = []
    for player_i in range(n_players):   # Get all old/new coordinates
        if state.status[player_i] == 'dead':
            heads.append("Dead")
            tails.append("Dead")
            continue
        head_x = (state.snakes[player_i][-1][0] +
                     direction_x[new_moves[player_i]] + width) % width
        head_y = (state.snakes[player_i][-1][1] +
                     direction_y[new_moves[player_i]] + height) % height
        
        next_pos = maze[head_y][head_x]

        # check if snake collides with itself
        
        if next_pos == str(player_i):
            if state.snakes[player_i][0][0] == head_x and state.snakes[player_i][0][1] == head_y and len(state.snakes[player_i]) != 2:
                pass
                #no collision; on own tail (unless it has length 2)
            else:
                game_log.write("Player "+str(player_i)+" collided with himself! " + "\n")
                state.status[player_i] = 'dead'
                heads.append("Dead")
                tails.append("Dead")
                continue
                #self collision
        #TODO: check above code (is 0 x and 1 y? is it in the correct position, etc)

        heads.append([head_x, head_y])
        if next_pos == 'x':
            tails.append("None") # A snake that eats has no "tail"
        else:
            tails.append(state.snakes[player_i][0])

    game_log.write("Heads: "+str(heads) + "\n")#DEBUG
    game_log.write("Tails: "+str(tails) + "\n")#DEBUG
    
    for player_i in range(n_players):
        if state.status[player_i] == 'dead':
            continue

        head_x = heads[player_i][0]
        head_y = heads[player_i][1]

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
            state.snakes[player_i].append([head_x, head_y])
            maze[head_y][head_x] = str(player_i)
            if next_pos != 'x': # If no food is eaten, we must remove the tail
                tail=state.snakes[player_i].pop(0)
                maze[tail[1]][tail[0]] = '.'
        else: # We must have collided (note that you can collide with a dead snake)
            state.status[player_i] = 'dead'
            players[player_i].sendline("quit") # Gently stop the process
            if player_i == 0:
                debug_out.write("quit"+"\n")
            game_log.write("Player "+str(player_i)+" died!\n")
            # TODO: remove body of dead snake?
            # TODO: force program to exit as well?

        #TODO: stop iteration if all players are dead or if game stagnates
        #TODO: scoring


for i in range(n_players):
    player_logs_send[i].close()
    player_logs_read[i].close()
game_log.close()
