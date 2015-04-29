#!/bin/python
import random
import fileinput


###Initialisatie

level_hoogte = int(input())         #Lees hoe groot het level is
level_breedte = int(input())

level = []                          #Lees het level regel voor regel
for y in range(level_hoogte):
    level.append(input())

aantal_spelers = int(input())       #Lees het aantal spelers en hun posities
begin_posities = []
for i in range(aantal_spelers):
    begin_positie = [int(s) for s in input().split()]
    begin_posities.append(begin_positie)

speler_nummer = int(input())        #Lees onze beginpositie


###De tijdstap
pos = begin_posities[speler_nummer]

while True:
    for i in range(15):
        if i == 0:
            i += int(random.choice('0123'))
        if i == 99:
            print('move')
            print('u')
            break

        x = pos[0]
        y = pos[1]
        c = 'udlr'[i%4]#random.choice('udlr')
        if c == 'u':
            y = (y-1+level_hoogte)%level_hoogte
            x = (x  +level_breedte)%level_breedte
        if c == 'd':
            y = (y+1+level_hoogte)%level_hoogte
            x = (x  +level_breedte)%level_breedte
        if c == 'l':
            y = (y  +level_hoogte)%level_hoogte
            x = (x-1+level_breedte)%level_breedte
        if c == 'r':
            y = (y  +level_hoogte)%level_hoogte
            x = (x+1+level_breedte)%level_breedte

        if level[y][x] == '.':
            print('move')
            print(c)    #Beweeg! u=up, d=down, l=left, r=right
            pos = [x, y]
            break
            
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

