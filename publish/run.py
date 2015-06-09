#!/usr/bin/python3
import pexpect
import sys
import signal

sys.path.append('../viewer')
import mazes
import snapshot

print("Python Snake Challenge V1")

width = int(input("Level width? "))
height = int(input("Level height? "))
if width < 10 or height < 10:
    print("Level too small! Defaulted to width = 10 and height = 10.")
    width = 10
    height = 10
n_players = int(input("How many players? "))
if n_players > 8:
    print("Too many players! There will be 8 players.")
    n_players = 8

print("Assuming you have more than " + str(n_players) + " cores..")

player_bins = ["python #human" for x in range(n_players)]
for i in range(n_players):
    player_bins[i] = input("Filename of player "+str(i)+" (type '#human' for a human player): ")
    if player_bins[i] != '#human':
        player_bins[i] = "python3 "+player_bins[i]
    else:
        print("Player "+str(i)+" is human, you can steer using wsad")

max_mem = 100000                                        # memory beschikbaar voor spelers in kb
core_ids = [hex(1<<x) for x in range(n_players)]      # namen van cores
                                                        # start restricted processen voor spelers
players = [pexpect.spawnu("./timeout -m "+str(max_mem)+" taskset "+core_ids[x]+" "+player_bins[x]) for x in range(n_players)]
player_logs_send = [open("logs/in"+str(i)+".txt", 'w') for i in range(n_players)]
player_logs_read = [open("logs/all"+str(i)+".txt", 'w') for i in range(n_players)]
game_log = open("logs/game.txt", 'w')

for i in range(n_players):
    players[i].logfile_send = player_logs_send[i]
    players[i].logfile_read = player_logs_read[i]

# maze stores players, food, walls and open space
maze = mazes.generate_maze(width,height,0.1)

# Store state in snapshot
state = snapshot.Snapshot()
state.width = width
state.height = height
state.content = maze
state.names = [player_bin[7:min(14,len(player_bin)-3)] for player_bin in player_bins]
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

n_food_iter = max(int(n_players/4),1)

max_timesteps = 500
old_moves = ""
spawn_food = []

def _find_getch():
    try:
        import termios
    except ImportError:
        # Non-POSIX. Return msvcrt's (Windows') getch.
        import msvcrt
        return msvcrt.getch

    # POSIX system. Create and return a getch that manipulates the tty.
    import sys, tty
    def _getch():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

    return _getch
getch = _find_getch()

# The time step
for timestep in range(max_timesteps):
    game_log.write("TIMESTEP "+str(timestep)+"\n")
    mazes.show_maze(maze, game_log)
    print("\nTimestep "+str(timestep))
    mazes.show_maze(maze)
    game_log.write("/TIMESTEP "+str(timestep)+"\n")
    # We will obtain new_moves after passing old_moves to the players

    # TODO: make symmetric, make sure amounts are right (will crash when no space left!)
    new_moves = ["?"]*n_players

    player_order = sorted([[state.scores[i], i] for i in range(n_players)])
    for index in range(n_players): 
        player_i = player_order[index][1]

        if state.status[player_i] == 'dead':
            new_moves[player_i] = 'x'
            continue

        p = players[player_i]

        # Send moves + new food coordinates
        if len(old_moves) > 0:
            update_string = ""
            update_string += "".join(old_moves) + "\n"
            update_string += str(len(spawn_food)) + "\n"
            update_string += "\n".join([str(food[0]) + " " + str(food[1]) for food in spawn_food])
            p.sendline(update_string)
        
        # Read moves
        try:
            if player_bins[player_i] == "#human":   #For humans only!
                char = getch()
                direction_index = "wsad".find(char)
            else:
                p.expect("move", timeout=1)
                direction_index = p.expect(direction_chars, timeout=1)
        except:
            game_log.write("Player "+str(player_i)+"'s AI crashed!\n")
            game_log.write("As a result, player "+str(player_i)+" has been declared dead\n")
            state.status[player_i] = 'dead'
            new_moves[player_i] = 'x'
            for i in range(n_players):
                if state.status[i] != 'dead':
                    state.scores[i] += 1000   #Score +1000 if other player dies
            continue
        # TODO: check for timeout!
        new_moves[player_i] = direction_chars[direction_index]

    old_moves = new_moves
    
    game_log.write("Moves to be executed: " + "".join(new_moves) + "\n")

    # Update snapshot
    for index in range(n_players):   # Move all players (low scores move first)
        player_i = player_order[index][1]

        print("moving "+str(player_i) + "(with "+str(state.scores[player_i])+" points)")
        game_log.write("Player "+str(player_i) + " has "+str(state.scores[player_i])+" points\n")
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
                state.food.remove([head_x,head_y])
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

    # Spawn new food
    spawn_food = [mazes.get_empty_cell(maze, width, height, 'x') for x in range(n_food_iter)]
    spawn_food = [food for food in spawn_food if food != 0] #get_empty_cell returns 0 if no empty spot is found
    state.food.extend(spawn_food)

    # Check if we need to terminate the game
    n_players_left = n_players
    for i in range(n_players):
        if state.status[i] == 'dead':
            n_players_left -= 1
    if n_players_left == 0: #stop iteration if all players are dead or if game stagnates
        game_log.write("All players are dead!\n")
        break
    state.save("logs/state.dat")

game_log.write("The game has ended!\n")
for i in range(n_players):
    game_log.write("Player "+str(i)+" has "+str(state.scores[i])+"pts\n")

for i in range(n_players):
    player_logs_send[i].close()
    player_logs_read[i].close()

game_log.close()
