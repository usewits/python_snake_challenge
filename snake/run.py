#!/bin/python
import pexpect
import sys

sys.path.append('../viewer')
import mazes
import snapshot

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

# Initialize players
for player_i in range(n_players):
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
        # TODO: check for timeout!
        new_moves += direction_chars[direction_index]

    old_moves = new_moves
    spawn_food = [mazes.get_empty_cell(maze, width, height, 'x') for x in range(n_food_iter)]
    
    game_log.write("Moves to be executed: " + new_moves + "\n")


    # Update snapshot
    player_order = sorted([[state.scores[i], i] for i in range(n_players)])
    for index in range(n_players):   # Move all players (low scores move first)
        player_i = player_order[index][1]
        print("moving "+str(player_i))
        if state.status[player_i] == 'dead':
            continue
        head_x = (state.snakes[player_i][-1][0] +
                     direction_x[new_moves[player_i]] + width) % width
        head_y = (state.snakes[player_i][-1][1] +
                     direction_y[new_moves[player_i]] + height) % height
        
        next_pos = maze[head_y][head_x]

        # check if snake collides with itself
        
        if next_pos == '.' or next_pos == 'x':
            state.snakes[player_i].append([head_x, head_y])
            maze[head_y][head_x] = str(player_i)
            if next_pos != 'x': # If no food is eaten, we must remove the tail
                tail=state.snakes[player_i].pop(0)
                maze[tail[1]][tail[0]] = '.'
                state.scores[player_i] += 1     #Score +1 if valid move is performed
            else:
                state.scores[player_i] += 100    #Score +100 if food is consumed

        else:
            game_log.write("Player "+str(player_i)+" ")
            if next_pos == str(player_i):
                game_log.write("killed himself!\n")
            elif next_pos == '#':
                game_log.write("ran into a wall!\n")
            else:#must be other player
                other_player = int(next_pos)
                game_log.write("was killed by player "+str(other_player)+"!\n")
                
            players[player_i].sendline("quit") # Gently stop the process
            state.status[player_i] = 'dead'
            for i in range(n_players):
                if state.status[i] != 'dead':
                    state.scores[i] += 1000   #Score +1000 if other player dies
            continue
            # TODO: remove body of dead snake?
            # TODO: force program to exit as well?

    n_players_left = n_players
    for i in range(n_players):
        if state.status[i] == 'dead':
            n_players_left-=1
    if n_players_left == 0: #stop iteration if all players are dead or if game stagnates
        game_log.write("All players are dead!\n")
        break

game_log.write("The game has ended!\n")
for i in range(n_players):
    game_log.write("Player "+str(i)+" has "+str(state.scores[i])+"pts\n")

for i in range(n_players):
    player_logs_send[i].close()
    player_logs_read[i].close()

game_log.close()
