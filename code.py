import sys
from collections import namedtuple
import math

MAX_X =17630
MAX_Y =9000

def Dist(x1,y1,x2,y2):
    return math.sqrt(pow((y2-y1), 2)+pow((x2-x1), 2))

Entity = namedtuple('Entity', [
    'id', 'type', 'x', 'y', 'shield_life', 'is_controlled', 'health', 'vx', 'vy', 'near_base', 'threat_for'
])

TYPE_MONSTER = 0
TYPE_MY_HERO = 1
TYPE_OP_HERO = 2

# base_x,base_y: The corner of the map representing your base
base_x, base_y = [int(i) for i in input().split()]
heroes_per_player = int(input())

# game position
def x_start(x):
    return abs(base_x - x)
def y_start(y):
    return abs(base_y - y)
def x_opp_base():
    return abs((base_x - MAX_X))
def y_opp_base():
    return abs((base_y - MAX_Y))

# game loop
while True:
    my_health, my_mana = [int(j) for j in input().split()]
    enemy_health, enemy_mana = [int(j) for j in input().split()]
    entity_count = int(input())  # Amount of heros and monsters you can see

    monsters = []
    my_heroes = []
    opp_heroes = []
    for i in range(entity_count):
        _id, _type, x, y, shield_life, is_controlled, health, vx, vy, near_base, threat_for = [int(j) for j in input().split()]
        entity = Entity(
            _id,            # _id: Unique identifier
            _type,          # _type: 0=monster, 1=your hero, 2=opponent hero
            x, y,           # x,y: Position of this entity
            shield_life,    # shield_life: Ignore for this league; Count down until shield spell fades
            is_controlled,  # is_controlled: Ignore for this league; Equals 1 when this entity is under a control spell
            health,         # health: Remaining health of this monster
            vx, vy,         # vx,vy: Trajectory of this monster
            near_base,      # near_base: 0=monster with no target yet, 1=monster targeting a base
            threat_for,     # threat_for: Given this monster's trajectory, is it a threat to 1=your base, 2=your opponent's base, 0=neither
        )

        if _type == TYPE_MONSTER:
            monsters.append(entity)
        elif _type == TYPE_MY_HERO:
            my_heroes.append(entity)
        elif _type == TYPE_OP_HERO:
            opp_heroes.append(entity)

    target_1 = None
    target_2 = None
    target_3 = None

    for monster in monsters:
        if target_3 == None and Dist(base_x,base_y,monster.x,monster.y) < 7000:
            target_3 = monster
            continue
        elif target_3 != None:
            if Dist(base_x,base_y,monster.x,monster.y) < Dist(base_x,base_y,target_3.x,target_3.y) and not monster.is_controlled:
                target_3 = monster
                continue
        if target_2 is None and monster.threat_for == 0:
            target_2 = monster
            continue
        elif target_2 is not None:
            if Dist(x_opp_base(), y_opp_base(), monster.x, monster.y) < Dist(x_opp_base(), y_opp_base(), target_2.x, target_2.y) and monster.threat_for == 1:
                target_1 = monster
                continue
            if Dist(x_opp_base(), y_opp_base(), monster.x, monster.y) < Dist(x_opp_base(), y_opp_base(), target_2.x, target_2.y)  and not monster.is_controlled:
                target_2 = monster
                continue
        if target_1 is None:
            target_1 = monster
        elif target_1 is not None:
            if Dist(base_x, base_y, monster.x, monster.y) < Dist(base_x, base_y, target_1.x, target_1.y) and monster.threat_for == 1 and not monster.is_controlled:
                target_1 = monster
    #player 1

    if target_1 == None:
        print("MOVE {} {}".format(x_start(4000), y_start(7000)))
    elif target_1.threat_for == 1 and my_mana > 20:
        print("SPELL CONTROL {} {} {}".format(target_1.id, x_opp_base(), y_opp_base()))
    else:
        print("MOVE {} {}".format(target_1.x, target_1.y))

    #player 2

    if target_2 == None:
        print("MOVE {} {}".format(x_start(10000), y_start(6000)))
    elif target_2.threat_for == 0 and my_mana > 20:
        print("SPELL CONTROL {} {} {}".format(target_2.id, x_opp_base(), y_opp_base()))
    elif target_2.threat_for == 2 and my_mana > 20:
        print("SPELL WIND {} {}".format(x_opp_base(), y_opp_base()))
    else:
        print("MOVE {} {}".format(target_2.x, target_2.y))

    #player 3

    if target_3 == None:
        print("MOVE {} {}".format(x_start(4300), y_start(3300)))
    elif Dist (my_heroes[2].x, my_heroes[2].y, target_3.x, target_3.y) < 1280 and my_mana > 20 and target_3.threat_for == 1 :
        print("SPELL WIND {} {}".format(x_opp_base(), y_opp_base()))
    else:
        print("MOVE {} {}".format(target_3.x, target_3.y))
