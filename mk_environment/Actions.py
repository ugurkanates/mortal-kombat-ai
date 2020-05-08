from enum import Enum
from MAMEToolkit.emulator import Action


# An enumerable class used to specify which actions can be used to interact with a game
# Specifies the Lua engine port and field names required for performing an action
class Actions(Enum):
    # Starting
    SERVICE = Action(':INPUTS', 'Service Mode')

    COIN_P1 = Action(':INPUTS', 'Coin 1')
    COIN_P2 = Action(':INPUTS', 'Coin 2')

    P1_START = Action(':INPUTS', '1 Player Start')
    P2_START = Action(':INPUTS', '2 Players Start')

    # Movement
    P1_UP = Action(':IN0', 'P1 Up')
    P1_DOWN = Action(':IN0', 'P1 Down')
    P1_LEFT = Action(':IN0', 'P1 Left')
    P1_RIGHT = Action(':IN0', 'P1 Right')

    P2_UP = Action(':IN0', 'P2 Up')
    P2_DOWN = Action(':IN0', 'P2 Down')
    P2_LEFT = Action(':IN0', 'P2 Left')
    P2_RIGHT = Action(':IN0', 'P2 Right')

    # Fighting
    P1_HIGH_PUNCH = Action(':IN0', 'P1 High Punch')
    P1_SPUNCH = Action(':INPUTS', 'P1 Strong Punch')
    P1_FPUNCH = Action(':INPUTS', 'P1 Fierce Punch')
    P1_HIGH_KICK = Action(':IN0', 'P1 High Kick')
    P1_LOW_KICK = Action(':IN1', 'P1 Low Kick')
    P1_RKICK = Action(':EXTRA', 'P1 Roundhouse Kick')

    P2_JPUNCH = Action(':INPUTS', 'P2 Jab Punch')
    P2_SPUNCH = Action(':INPUTS', 'P2 Strong Punch')
    P2_FPUNCH = Action(':INPUTS', 'P2 Fierce Punch')
    P2_SKICK = Action(':EXTRA', 'P2 Short Kick')
    P2_FKICK = Action(':EXTRA', 'P2 Forward Kick')
    P2_RKICK = Action(':INPUTS', 'P2 Roundhouse Kick')


[{'port': ':DSW', 'field': 'Skip Post Test'}, {'port': ':DSW', 'field': 'Counters'}, {'port': ':DSW', 'field': 'Low Blows'}, {'port': ':DSW', 'field': 'Attract Sound'}, {'port': ':DSW', 'field': 'Violence'}, {'port': ':DSW', 'field': 'Blood'}, {'port': ':DSW', 'field': 'Unused'}, {'port': ':DSW', 'field': 'Comic Book Offer'}, {'port': ':DSW', 'field': 'Test Switch'}, {'port': ':DSW', 'field': 'Coinage Source'}, {'port': ':DSW', 'field': 'Coinage'}, {'port': ':IN0', 'field': 'P2 High Kick'}, {'port': ':IN0', 'field': 'P2 Down'}, {'port': ':IN0', 'field': 'P2 Block'}, {'port': ':IN0', 'field': 'P2 High Punch'}, {'port': ':IN0', 'field': 'P1 High Kick'}, {'port': ':IN0', 'field': 'P2 Left'}, {'port': ':IN0', 'field': 'P1 Right'}, {'port': ':IN0', 'field': 'P2 Right'}, {'port': ':IN0', 'field': 'P2 Up'},
    {'port': ':IN0', 'field': 'P1 High Punch'}, {'port': ':IN0', 'field': 'P1 Up'}, {'port': ':IN0', 'field': 'P1 Left'}, {'port': ':IN0', 'field': 'P1 Down'}, {'port': ':IN0', 'field': 'P1 Block'}, {'port': ':IN1', 'field': 'P1 Block 2'}, {'port': ':IN1', 'field': 'Tilt'}, {'port': ':IN1', 'field': 'Service 1'}, {'port': ':IN1', 'field': 'P1 Low Kick'}, {'port': ':IN1', 'field': 'P2 Low Kick'}, {'port': ':IN1', 'field': 'P2 Low Punch'}, {'port': ':IN1', 'field': 'P2 Block 2'}, {'port': ':IN1', 'field': 'Coin 2'}, {'port': ':IN1', 'field': 'Coin 1'}, {'port': ':IN1', 'field': 'P1 Low Punch'}, {'port': ':IN1', 'field': 'Service Mode'}, {'port': ':IN1', 'field': '1 Player Start'}, {'port': ':IN1', 'field': '2 Players Start'}, {'port': ':IN1', 'field': 'Coin 3'}, {'port': ':IN1', 'field': 'Coin 4'}]
