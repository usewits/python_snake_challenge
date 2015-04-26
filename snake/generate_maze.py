import random

def generate_maze(w, h, global_density = 0.4, local_density = 2):
    level = [['.' for x in range(w)] for y in range(h)]
    for i in range(int(global_density*w*h)):
        while True:
            x = random.randint(1,w)-1
            y = random.randint(1,h)-1
            if level[y][x] != '.':
                continue
            c = 0
            for dx in range(-1,2):
                for dy in range(-1,2):
                    if level[(y+dy+h)%h][(x+dx+w)%w] != '.':
                        c+=1
            if c > local_density:
                continue
            level[y][x] = '#'
            break
    return level

def generate_maze2(w, h):
    maze = [[".#"[(x%2)*(y%2)] for x in range(w)] for y in range(h)]
    return maze

def show_maze(maze):
    for line in maze:
        print("".join(line))
