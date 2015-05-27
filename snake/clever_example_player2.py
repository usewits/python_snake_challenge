#!/bin/python
import random
import fileinput


###Initialisatie

level_hoogte = int(input())         #Lees hoe groot het level is
level_breedte = int(input())

level = []                          #Lees het level regel voor regel
for y in range(level_hoogte):
    level.append(list(input()))

aantal_spelers = int(input())       #Lees het aantal spelers en hun posities
begin_posities = []
for i in range(aantal_spelers):
    begin_positie = [int(s) for s in input().split()]
    begin_posities.append(begin_positie)

speler_nummer = int(input())        #Lees onze beginpositie


###Snake

class snake:
    index = -1
    positie = []
    alive = True

    def __init__(self, index, head):
        self.index = index
        self.positie = [head]
        self.alive = True
    
    def move(self, pos, next_field):
        print("state:")#DEBUG
        print(self.positie)#DEBUG
        for row in level:
            print("".join(row))
        print("moving to:"+next_field)#DEBUG
        print(str(pos[0])+","+str(pos[1]))#DEBUG
        if not self.alive:
            return
        if next_field == '.' or next_field == 'x':
            level[pos[1]][pos[0]] = str(self.index)
            self.positie.append(pos)
            if next_field == '.':
                level[self.positie[0][1]][self.positie[0][0]] = '.'
                self.positie.pop(0)
        if next_field == '#':
            self.alive = False
            return


###De tijdstap

pos = begin_posities[speler_nummer]
dx = [ 0, 1, 0,-1]
dy = [-1, 0, 1, 0]

state = snake(speler_nummer, pos)

while True:
    k = int(random.choice('0123'))
    moved = False
    for j in range(4):
        i = (j+k)%4
        c = 'urdl'[i]
        head = list(state.positie[-1])
        head[0] += dx[i]
        head[1] += dy[i]
        head[0] = (head[0] + level_breedte)% level_breedte
        head[1] = (head[1] + level_hoogte) % level_hoogte
        next_field = level[head[1]][head[0]]
        if next_field  == '.' or next_field == 'x':
            state.move(head, next_field)
            print('move')
            print(c)    #Beweeg! u=up, d=down, l=left, r=right
            moved = True
            break

    if not moved:
        print('move')
        print('u')      #Beweeg, ook al werkt dit niet


    line = input()                  #Lees nieuwe informatie
    if line == "quit":
        print("bye")
        break

    speler_bewegingen = line        #String met bewegingen van alle spelers

    aantal_voedsel = int(input())   #Lees aantal nieuw voedsel en posities
    voedsel_posities = []
    for i in range(aantal_voedsel):
        voedsel_positie = [int(s) for s in input().split()]
        voedsel_posities.append(voedsel_positie)
        level[voedsel_positie[1]][voedsel_positie[0]] = "x"

