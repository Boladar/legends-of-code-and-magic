import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.
class Card:
    def __init__(self, card_number, instance_id, location, card_type, cost, attack, defense, abilities, my_health_change, opponent_health_change, card_draw):
        self.card_number = card_number
        self.instance_id = instance_id
        self.location = location
        self.card_type = card_type
        self.cost = cost
        self.attack = attack
        self.defense = defense
        self.defense_left = defense
        self.abilities = abilities
        self.my_health_change = my_health_change
        self.opponent_health_change = opponent_health_change
        self.card_draw = card_draw
        self.health_change = 0
        self.used = False

class Player:
    def __init__(self,player_health = 0, player_mana = 0, player_deck = 0, player_rune = 0, player_draw = 0,command = ""):
        self.health = player_health
        self.mana = player_mana
        self.leftMana = player_mana
        self.deck = player_deck
        self.rune = player_rune
        self.draw = player_draw
        self.command = command
    
    def updatePlayerParameters(self,player_health, player_mana, player_deck, player_rune, player_draw):
        self.health = player_health
        self.mana = player_mana
        self.leftMana = player_mana
        self.deck = player_deck
        self.rune = player_rune
        self.draw = player_draw
        self.command = ""

class Cell:
    def __init__(self):
        self.defense = 0
        self.WAP = 0
        self.flag = 0

def WPA(allies:[],enemies:[]):

    enemies.sort(key=lambda x: x.attack,reverse=True)
    allies.sort(key=lambda x: x.defense,reverse=True)

    A = []
    row = []
    for r in range(len(allies)):
        for c in range(len(enemies)):
            cell = Cell()
            row.append(cell)
        A.append(row)
        row = []

    for r in range(len(allies)):
        for c in range(len(enemies)):
            if r-1>=0 and ( A[r-1][c].flag == -1 or A[r-1][c].flag == -2 ):
                A[r][c].flag = -2
                continue

            cell = A[r][c]

            log("(" + str(r) + "," + str(c) + ")" + "attack: " + str(allies[r].attack) + ", defense" + str(enemies[c].defense))
            cell.WAP = allies[r].attack - enemies[c].defense
            log("cell wap: " + str(cell.WAP))

            if(r-1 >= 0):
                if A[r-1][c].flag < 0:
                    cell.WAP = allies[r].attack - enemies[c].defense
                elif r-1 and A[r-1][c].flag >= 0:
                    cell.WAP = allies[r].attack - A[r-1][c].defense

            if cell.WAP > 0:
                cell.defense = 0
            else:
                cell.defense = abs(cell.WAP)
            cell.flag = -3           
        #look for the best
        minWAP = 10000
        best_c_index = -1
        for c in range(len(enemies)):
            cell = A[r][c]
            if(abs(cell.WAP) < minWAP):
                if (r-1 >= 0 and A[r-1][c].flag >= 0 or A[r-1][c].flag == -3) or r == 0:
                    minWAP = abs(cell.WAP)
                    best_c_index = c

        if best_c_index != -1:
            if A[r][best_c_index].WAP == 0:
                A[r][best_c_index].flag = -1
            elif A[r][best_c_index].defense > 0:
                A[r][best_c_index].flag = r
                
            Player.command += "ATTACK " + str(allies[r].instance_id) +" " + str(enemies[best_c_index].instance_id) + ";"  
            allies[r].used = True

    for r in range(len(allies)):
        print(" ",file=sys.stderr)
        for c in range(len(enemies)):
            print("(" + str(A[r][c].defense) + "," + str(A[r][c].WAP) + "," + str(A[r][c].flag) + ")",end=" ", file=sys.stderr)

    #return
    

class General:
    def __init__(self):
        self.Cards_list = []
        self.allies = []
        self.enemies = []
        self.summoned = []

    def Update(self, Cards_list):
        self.allies = []
        self.enemies = []
        self.summoned = []
        self.Cards_list = Cards_list

        for card in Cards_list:
            if(card.location == 1):
                self.allies.append(card)
            elif (card.location == -1):
                self.enemies.append(card)

        self.enemies.sort(key=lambda x: x.attack,reverse=True)
        self.allies.sort(key=lambda x: x.attack,reverse=True)

    def Summon(self):
        canBeSummoned = []
        deck = []

        for card in self.Cards_list:
            if(card.location == 0 and card.card_type == 0):
                deck.append(card)

        for card in deck:
            if(Player.mana >= card.cost):   
                canBeSummoned.append(card)
        print("number of summonable creatures:" + str(len(canBeSummoned)),file=sys.stderr)

        canBeSummoned.sort(key= lambda x: x.cost,reverse = True)

        for s in canBeSummoned:
            if(Player.leftMana >= s.cost):
                Player.leftMana -= s.cost
                self.summoned.append(s)
                Player.command += "SUMMON " + str(s.instance_id) + ";"

    def CountEnemyAttackPotential(self) ->int:
        potential = 0
        for e in self.enemies:
            potential += e.attack
        return potential

    def CountAlliedAttackPotential(self) ->int:
        potential = 0
        for a in self.allies:
            potential += a.attack
        return potential

def Draft(Cards_list):

    most_valuable_index = -1
    attack_to_cost = -1

    for c in Cards_list:
        if(c.cost != 0):
            if((c.attack + c.defense )/ c.cost > attack_to_cost):
                attack_to_cost = (c.attack + c.defense)/ c.cost
                most_valuable_index = Cards_list.index(c)
        else:
            if((c.attack + c.defense) > attack_to_cost):
                attack_to_cost = c.attack + c.defense
                most_valuable_index = Cards_list.index(c)

    print ("PICK " + str(most_valuable_index)) 

def log(text):
    print(text,file=sys.stderr)

def Use(Cards_list):
    green = []
    red = []
    blue = []

    for card in Cards_list:
        if (card.card_type == 1):
            green.append(card)
        elif (card.card_type == 2):
            red.append(card)
        elif (card.card_type == 3):
            blue.append(card)

    if(len(General.enemies) > 0):
        strongest_enemy = General.enemies[0]
        #find strongest enemy
        for e in General.enemies:
            if(e.attack > strongest_enemy.attack):
                strongest_enemy = e

        for r in red:
            Player.command +="USE " + str(r.instance_id) + " " + str(strongest_enemy.instance_id) + ";"

    if(len(General.allies) > 0):
        strongest_ally = General.allies[0]
        #find strongest ally
        for a in General.allies:
            if(a.attack > strongest_ally.attack):
                strongest_ally = a
        for a in General.summoned:
            if(a.attack > strongest_ally.attack):
                strongest_ally = a

        for g in green:
            Player.command += "USE " + str(g.instance_id) + " " + str(strongest_ally.instance_id) + ";"
    
    for b in blue:
        Player.command += "USE " + str(b.instance_id) + " -1;"

def FindKillableOponent(unit: Card):
    #TODO: CHANGE
    target = General.enemies[0]
    for e in General.enemies:
        if(unit.attack >= e.defense and e.attack < unit.defense):
            target = e
    return target

def Attack(Cards_list):
    global OPONNENT_HEALTH

    log ("allies: " + str(len(General.allies)))
    log ("enemies: " + str(len(General.enemies)))

    guardians = []
    notGuardians = []
    for enemy in General.enemies:
        if(str(enemy.abilities).find("G") != -1):
            guardians.append(enemy)
        else:
            notGuardians.append(enemy)
    log("guardians: " + str(len(guardians)))

    WPA(General.allies,guardians)

    notUsed = []
    for ally in General.allies:
        if ally.used == False:
            notUsed.append(ally)

    log("not used: " + str(len(notUsed)))
    WPA(notUsed,notGuardians)

    notUsed = []
    for ally in General.allies:
        if ally.used == False:
            notUsed.append(ally)

    for n in notUsed:
        m = "ATTACK " + str(n.instance_id) + " -1;"
        Player.command += m

def Battle(Cards_list):
    log("BATTLE")
    General.Summon()
    Use(Cards_list)

    Attack(Cards_list)

    log ( "player.command: " + str(len(Player.command)))
    if(len(Player.command) == 0):
        print("PASS")
    elif(len(Player.command) > 0):
        print(Player.command)


def AnalyzeOponnentActions(Cards_list,actions_to_analyze):
    global OPONNENT_HEALTH
    for action in actions_to_analyze:
        if(action.find("SUMMON") != -1 or action.find("USE") != -1):
            instance = action[-2:]
            for c in Cards_list:
                if( c.instance_id == int(instance.replace(" ",""))):
                    OPONNENT_HEALTH += int(c.opponent_health_change)

#GLOBAL VARIABLES //////////////////////////////////////
General = General()
Player = Player()
TURN = 0
OPONNENT_HEALTH = 30
MAX_SUMMONED = 6
MAX_HAND_SIZE = 8
MAX_ITEMS = 5
#///////////////////////////////////////////////////////
# game loop
while True:
    for i in range(2):
        player_health, player_mana, player_deck, player_rune, player_draw = [int(j) for j in input().split()]
    
    #update Global Classes
    Player.updatePlayerParameters(player_health, player_mana, player_deck, player_rune, player_draw)
    
    actions_to_analyze = []
    opponent_hand, opponent_actions = [int(i) for i in input().split()]
    for i in range(opponent_actions):
        card_number_and_action = input()
        actions_to_analyze.append(card_number_and_action)
    card_count = int(input())

    Cards_list = []
    for i in range(card_count):
        card_number, instance_id, location, card_type, cost, attack, defense, abilities, my_health_change, opponent_health_change, card_draw = input().split()
        card_number = int(card_number)
        instance_id = int(instance_id)
        location = int(location)
        card_type = int(card_type)
        cost = int(cost)
        attack = int(attack)
        defense = int(defense)
        my_health_change = int(my_health_change)
        opponent_health_change = int(opponent_health_change)
        card_draw = int(card_draw)

        Cards_list.append(Card(card_number, instance_id, location, card_type, cost, attack, defense, abilities, my_health_change, opponent_health_change, card_draw))
    
    #update deck parameters
    AnalyzeOponnentActions(Cards_list,actions_to_analyze)
    General.Update(Cards_list)

    log("TURN: " + str(TURN))    
    log("ENEMY HEALTH: " + str(OPONNENT_HEALTH))

    if(len(General.allies)>0):
        log("STRONGEST ALLY: " + str(General.allies[0].instance_id))
    if(TURN < 30):
        Draft(Cards_list)
    else:
        Battle(Cards_list)
    
    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)

    TURN += 1
    #print("PASS")