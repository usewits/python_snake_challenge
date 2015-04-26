#!/bin/python
import pexpect

import generate_maze

player_bin = "python example_player.py"
max_mem = 100000        #in kb
core_ids = ["0x"+str(x) for x in range(4)]
players = [pexpect.spawn("./timeout -m "+str(max_mem)+" taskset "+core_ids[x]+" "+player_bin) for x in range(4)]

#TODO: now pipe in.txt to player

maze = generate_maze.generate_maze(1200,1200)

print(core_ids)
generate_maze.show_maze(maze)


