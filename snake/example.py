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

while True:
    print(random.choice('udlr'))    #Beweeg! u=up, d=down, l=left, r=right

    line = input()                  #Lees nieuwe informatie
    if line == "quit":              
        break

    speler_bewegingen = line        #String met bewegingen van alle spelers

    aantal_voedsel = int(input())   #Lees aantal nieuw voedsel en posities
    voedsel_posities = []
    for i in range(aantal_voedsel):
        voedsel_positie = [int(s) for s in input().split()]
        voedsel_posities.append(voedsel_positie)

