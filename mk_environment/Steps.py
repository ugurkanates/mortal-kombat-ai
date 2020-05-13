from .Actions import Actions
from .Characters import *
# A = Agent
# C = Computer
# H = Human
# An enurable class used to specify the set of action steps required to perform different predefined tasks
# E.g. changing the story mode difficulty, or starting a new game in single player story mode
def set_difficulty(frame_ratio, difficulty):
    steps = [
        {"wait": 0, "actions": [Actions.SERVICE]},
        {"wait": int(10/frame_ratio), "actions": [Actions.P1_DOWN]},
        {"wait": int(10/frame_ratio), "actions": [Actions.P1_DOWN]},
        {"wait": int(10/frame_ratio), "actions": [Actions.P1_DOWN]},
        {"wait": int(10/frame_ratio), "actions": [Actions.P1_DOWN]},
        {"wait": int(10/frame_ratio), "actions": [Actions.P1_DOWN]},
        {"wait": int(10/frame_ratio), "actions": [Actions.P1_DOWN]},
        {"wait": int(10/frame_ratio), "actions": [Actions.P1_JPUNCH]},
        {"wait": int(10/frame_ratio), "actions": [Actions.P1_DOWN]},
        {"wait": int(10/frame_ratio), "actions": [Actions.P1_JPUNCH]}]
    if (difficulty % 8) < 3:
        steps += [{"wait": int(10/frame_ratio), "actions": [Actions.P1_LEFT]} for i in range(3-(difficulty % 8))]
    else:
        steps += [{"wait": int(10/frame_ratio), "actions": [Actions.P1_RIGHT]} for i in range((difficulty % 8)-3)]
    steps += [
        {"wait": int(10/frame_ratio), "actions": [Actions.P1_DOWN]},
        {"wait": int(10/frame_ratio), "actions": [Actions.P1_DOWN]},
        {"wait": int(10/frame_ratio), "actions": [Actions.P1_DOWN]},
        {"wait": int(10/frame_ratio), "actions": [Actions.P1_DOWN]},
        {"wait": int(10/frame_ratio), "actions": [Actions.P1_DOWN]},
        {"wait": int(10/frame_ratio), "actions": [Actions.P1_DOWN]},
        {"wait": int(10/frame_ratio), "actions": [Actions.P1_JPUNCH]},
        {"wait": int(10/frame_ratio), "actions": [Actions.P1_DOWN]},
        {"wait": int(10/frame_ratio), "actions": [Actions.P1_JPUNCH]},
        {"wait": int(10/frame_ratio), "actions": [Actions.P1_DOWN]},
        {"wait": int(10/frame_ratio), "actions": [Actions.P1_DOWN]},
        {"wait": int(10/frame_ratio), "actions": [Actions.P1_JPUNCH]},
        {"wait": int(10/frame_ratio), "actions": [Actions.P1_DOWN]},
        {"wait": int(10/frame_ratio), "actions": [Actions.P1_DOWN]},
        {"wait": int(10/frame_ratio), "actions": [Actions.P1_DOWN]},
        {"wait": int(10/frame_ratio), "actions": [Actions.P1_JPUNCH]}]
    return steps

def select_character(character,frame_ratio):
    if character == Characters.SCORPION:
        returner = [{"wait": int(80/frame_ratio), "actions": [Actions.P1_RIGHT]},
                   {"wait": int(80/frame_ratio), "actions": [Actions.P1_DOWN]}]
    elif character == Characters.JOHNNY:
        returner = {"wait": int(80/frame_ratio), "actions": [Actions.P1_LEFT]}
    elif character == Characters.RAIDEN:
        returner = {"wait": int(80/frame_ratio), "actions": [Actions.P1_DOWN]}
    elif character == Characters.LIUKANG:
        returner = [{"wait": int(80/frame_ratio), "actions": [Actions.P1_DOWN]},
                   {"wait": int(80/frame_ratio), "actions": [Actions.P1_RIGHT]}]

    elif character == Characters.SONYA:
        returner = [{"wait": int(80/frame_ratio), "actions": [Actions.P1_RIGHT]},
                   {"wait": int(80/frame_ratio), "actions": [Actions.P1_RIGHT]}]

    #elif character == Characters.KANO:
     #   continue #blank he is default char just select


    return returner

def start_game(frame_ratio,character):
    ACTION_CHOSEN = select_character(character,frame_ratio)
    first_part = [
        {"wait": int(300/frame_ratio), "actions": [Actions.COIN_P1]},
        {"wait": int(10/frame_ratio), "actions": [Actions.COIN_P1]},
        {"wait": int(60/frame_ratio), "actions": [Actions.P1_START]}]
    first_part+= ACTION_CHOSEN
    second_part = {"wait": int(60/frame_ratio), "actions": [Actions.P1_HIGH_PUNCH]}
    third_part = {"wait": int(60/frame_ratio), "actions": [Actions.P1_HIGH_PUNCH]}
    first_part += [second_part]
    first_part += [third_part]
    return first_part

def next_stage(frame_ratio):
    return  [{"wait": int(60 / frame_ratio), "actions": [Actions.P1_JPUNCH]}] + \
            [{"wait": 0, "actions": [Actions.P1_JPUNCH]} for _ in range(int(180 / frame_ratio))] + \
            [{"wait": int(60/frame_ratio), "actions": [Actions.P1_JPUNCH]}]


def new_game(frame_ratio):
    return [{"wait": 0, "actions": [Actions.SERVICE]},
              {"wait": int(30 / frame_ratio), "actions": [Actions.P1_UP]},
              {"wait": int(30 / frame_ratio), "actions": [Actions.P1_JPUNCH]},
              {"wait": int(300 / frame_ratio), "actions": [Actions.COIN_P1]},
              {"wait": int(10 / frame_ratio), "actions": [Actions.COIN_P1]},
              {"wait": int(60 / frame_ratio), "actions": [Actions.P1_START]},
              {"wait": int(80 / frame_ratio), "actions": [Actions.P1_LEFT, Actions.P1_JPUNCH]},
              {"wait": int(60 / frame_ratio), "actions": [Actions.P1_JPUNCH]},
              {"wait": int(60 / frame_ratio), "actions": [Actions.P1_JPUNCH]}]
