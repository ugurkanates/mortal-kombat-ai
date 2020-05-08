from enum import Enum
from MAMEToolkit.emulator import Action


# An enumerable class used to specify which actions can be used to interact with a game
# Specifies the Lua engine port and field names required for performing an action
#  Reference for Mortal Kombat 1  Button Setup , thanks ^_^ 
# http://mameaddicts.com/phpBB3/viewtopic.php?t=526
class Actions(Enum):
    # Starting
    SERVICE = Action(':IN1', 'Service Mode')
    SKIP_POST = Action(':DSW', 'Skip Post Test')
    VIOLENCE = Action(':DSW', 'Violence')
    BLOOD = Action(':DSW', 'Blood')



    COIN_P1 = Action(':IN1', 'Coin 1')
    COIN_P2 = Action(':IN1', 'Coin 2')

    P1_START = Action(':IN1', '1 Player Start')
    P2_START = Action(':IN1', '2 Players Start')

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
    P1_LOW_PUNCH = Action(':IN1', 'P1 Low Punch')
    P1_BLOCK = Action(':IN0', 'P1 Block')
    P1_HIGH_KICK = Action(':IN0', 'P1 High Kick')
    P1_LOW_KICK = Action(':IN1', 'P1 Low Kick')

    P2_HIGH_PUNCH = Action(':IN0', 'P2 High Punch')
    P2_LOW_PUNCH = Action(':IN1', 'P2 Low Punch')
    P2_BLOCK = Action(':IN0', 'P2 Block')
    P2_HIGH_KICK = Action(':IN0', 'P2 High Kick')
    P2_LOW_KICK = Action(':IN1', 'P2 Low Kick')




      
