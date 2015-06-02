#!/bin/python
import random
import fileinput

###Initialisatie
# We lezen het doolhof en beginposities in

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

speler_nummer = int(input())        #Lees welk spelernummer wij zijn


###De tijdstap

# We beginnen op de volgende positie:
positie = begin_posities[speler_nummer]

# dx en dy geven aan in welke richting 'u', 'r', 'd' en 'l' zijn:
dx = [ 0, 1, 0,-1]
dy = [-1, 0, 1, 0]

while True:
    i = random.randrange(4)         #Kies een random richting
    richting = 'urdl'[i]            #u=up, d=down, l=left, r=right
    positie[0] += dx[i]             #Verander de huidige positie
    positie[1] += dy[i]
                                    #Let op periodieke randvoorwaarden!
    positie[0] = (positie[0] + level_breedte)% level_breedte
    positie[1] = (positie[1] + level_hoogte) % level_hoogte
    

    volgende_vakje = level[positie[1]][positie[0]]

    problemen = False
    honger = True
    if volgende_vakje == '#':
        # We lopen tegen een muur op!
        problemen = True
    elif volgende_vakje  == '.':
        # We lopen (waarschijnlijk) naar een leeg veld!
        problemen = False
    elif volgende_vakje == 'x':
        # We lopen naar voedsel!
        problemen = False
        honger = False
        # We onthouden alvast dat het vakje leeg zal worden:
        level[positie[1]][positie[0]] = '.'
    
    # We proberen te bewegen, ongeacht van eventuele problemen
    print('move')       #Geef door dat we gaan bewegen
    print(richting)     #Geef de richting door

    line = input()                  #Lees nieuwe informatie

    if line == "quit":              #We krijgen dit door als het spel is afgelopen
        print("bye")                #Geef door dat we dit begrepen hebben
        break

    speler_bewegingen = line        #String met bewegingen van alle spelers

    aantal_voedsel = int(input())   #Lees aantal nieuw voedsel en posities
    voedsel_posities = []
    for i in range(aantal_voedsel):
        voedsel_positie = [int(s) for s in input().split()]
        # Sla de voedsel positie op in een lijst en in het level
        voedsel_posities.append(voedsel_positie)
        level[voedsel_positie[1]][voedsel_positie[0]] = "x"

