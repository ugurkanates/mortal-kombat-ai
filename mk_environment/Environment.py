from MAMEToolkit.emulator import Emulator
from MAMEToolkit.emulator import Address
from .Steps import *
from .Actions import Actions
from .Characters import *
from .Image_Manipulation import *

ROUND_BONUS = 15
STAGE_BONUS = 50
GAME_END_BONUS = 100
# Combines the data of multiple time steps
def add_rewards(old_data, new_data):
    for k in old_data.keys():
        if "rewards" in k:
            for player in old_data[k]:
                new_data[k][player] += old_data[k][player]
    return new_data

def add_rewards_constant(data,amount):
    for k in data.keys():
        if "rewards" in k:
            for player in data[k]:
                data[k][player] += amount
    return data


# not used , here for not breaking legacy code.
def setup_memory_addresses():
    return {
        "fighting": Address('0x02011389', 'u8')
    }

# Converts and index (action) into the relevant movement action Enum, depending on the player
def index_to_move_action(action):
    return {
        0: [Actions.
        P1_LEFT],
        1: [Actions.P1_LEFT, Actions.P1_UP],
        2: [Actions.P1_UP],
        3: [Actions.P1_UP, Actions.P1_RIGHT],
        4: [Actions.P1_RIGHT],
        5: [Actions.P1_RIGHT, Actions.P1_DOWN],
        6: [Actions.P1_DOWN],
        7: [Actions.P1_DOWN, Actions.P1_LEFT],
        8: []
    }[action]


# Converts and index (action) into the relevant attack action Enum, depending on the player
def index_to_attack_action(action):
    return {
        0: [Actions.P1_HIGH_PUNCH],
        1: [Actions.P1_LOW_PUNCH],
        2: [Actions.P1_HIGH_KICK],
        3: [Actions.P1_LOW_KICK],
        4: [Actions.P1_BLOCK],
        5: []
    }[action]


# The Mortal Kombat specific interface for training an agent against the game
class Environment(object):

    # env_id - the unique identifier of the emulator environment, used to create fifo pipes
    # difficulty - the difficult to be used in story mode gameplay
    # frame_ratio, frames_per_step - see Emulator class
    # render, throttle, debug - see Console class
    def __init__(self, env_id, roms_path,game_id,difficulty=3, frame_ratio=60, frames_per_step=3, render=True, throttle=False, frame_skip=0, sound=False, debug=True, binary_path=None,character=Characters.SCORPION.value):
        self.difficulty = difficulty
        self.frame_ratio = frame_ratio
        self.frames_per_step = frames_per_step
        self.throttle = throttle
        self.emu = Emulator(env_id, roms_path,game_id, setup_memory_addresses(), frame_ratio=frame_ratio, render=render, throttle=throttle, frame_skip=frame_skip, sound=sound, debug=debug, binary_path=binary_path)
        self.started = False
        self.previous_health = {"P1": 0, "P2": 0} # difference between preHP and currentHP is
        self.previous_wins = {"P1": 0, "P2": 0}
        self.round_done = False
        self.stage_done = False
        self.game_done = False
        self.stage = 1
        self.character = character
        self.fullHP_p1 = Image.new(size=(0,0),mode="RGB")
        self.fullHP_p2 = Image.new(size=(0,0),mode="RGB")
        self.active_round = 0

    def startAfterFail(self):
        self.run_steps({"wait": int(10/self.frame_ratio), "actions": [Actions.COIN_P1]})
        frames = self.wait_for_fight_start()
        self.active_round = 1
        print("DEBUG , fight started detected")


    # Runs a set of action steps over a series of time steps
    # Used for transitioning the emulator through non-learnable gameplay, aka. title screens, character selects
    def run_steps(self, steps):
        for step in steps:
            for i in range(step["wait"]):
                self.emu.step([])
            self.emu.step([action.value for action in step["actions"]])

    # Must be called first after creating this class
    # Sends actions to the game until the learnable gameplay starts
    # Returns the first few frames of gameplay
    def start(self):
        if self.throttle:
            for i in range(int(250/self.frame_ratio)):
                self.emu.step([])
        #self.run_steps(set_difficulty(self.frame_ratio, self.difficulty))
        self.run_steps(start_game(self.frame_ratio,self.character))
        frames = self.wait_for_fight_start()
        self.started = True
        self.fullHP_p1 = get_health_bar(frames,1)
        self.fullHP_p2 = get_health_bar(frames,2)
        self.active_round = 1
        print("DEBUG , fight started detected")
        return True
    
    # Gets input data frame from mame
    # depending on selection of frames 1  or more for understanding motion
    # we always get 0 index pic 
    # returns False if frame didn't contain starting 99 or 98 timers
    # True if it does
    # @TODO error check -> data["frame"] = frames[0] if self.frames_per_step == 1 else frames
    def is_timer_appear(self,picture):
        cropped_img = crop_timer(picture)#[0])
        if (rmsdiffer(imgRemoveUtil(crop_timer_img,cropped_img))) > 0.25 :
            return True
        else:
            return False

    # Observes the game and waits for the fight to start
    def wait_for_fight_start(self):
        data = self.emu.step([])
        while self.is_timer_appear(data["frame"]):
            data = self.emu.step([])
        self.expected_health = {"P1": 1.0, "P2": 1.0}
        #data = self.gather_frames([])
        return data["frame"]

    def reset(self):
        if self.game_done:
            return self.new_game()
        elif self.stage_done:
            return self.next_stage()
        elif self.round_done:
            return self.next_round()
        else:
            raise EnvironmentError("Reset called while gameplay still running")

    # To be called when a round finishes
    # Performs the necessary steps to take the agent to the next round of gameplay
    def next_round(self):
        self.round_done = False
        self.expected_health = {"P1": 0, "P2": 0}
        return self.wait_for_fight_start()

    # To be called when a game finishes
    # Performs the necessary steps to take the agent(s) to the next game and resets the necessary book keeping variables
    def next_stage(self):
        self.wait_for_continue()
        self.run_steps(next_stage(self.frame_ratio))
        self.expected_health = {"P1": 0, "P2": 0}
        self.expected_wins = {"P1": 0, "P2": 0}
        self.round_done = False
        self.stage_done = False
        return self.wait_for_fight_start()

    def new_game(self):
        self.wait_for_continue()
        self.run_steps(new_game(self.frame_ratio))
        self.expected_health = {"P1": 0, "P2": 0}
        self.expected_wins = {"P1": 0, "P2": 0}
        self.round_done = False
        self.stage_done = False
        self.game_done = False
        self.stage = 1
        return self.wait_for_fight_start()

    # Steps the emulator along until the screen goes black at the very end of a game
    def wait_for_continue(self):
        data = self.emu.step([])
        if self.frames_per_step == 1:
            while data["frame"].sum() != 0:
                data = self.emu.step([])
        else:
            while data["frame"][0].sum() != 0:
                data = self.emu.step([])

    # Steps the emulator along until the round is definitely over
    def run_till_victor(self, data):
        while self.expected_wins["P1"] == data["winsP1"] and self.expected_wins["P2"] == data["winsP2"]:
            data = add_rewards(data, self.sub_step([]))
        self.expected_wins = {"P1":data["winsP1"], "P2":data["winsP2"]}
        return data

    # Checks whether the round or game has finished
    def check_done(self, data):
        # data["fighting"] =  kim kazandigini dondur p1 p2 countlara baakarak ve a little logic
        #  oyun bitince next stage kadar zaten oburu gorene kdr bekler
        # kaybedincede karakter sec oburunu goree kdr bekler same shit
        status,whoWin = checkRoundDone(data["frame"][0],self.active_round)
        if self.active_round == 1:
            if status == True :   # active_round completed 
                if whoWin == 1 :
                    self.previous_wins["P1"] += 1
                elif whoWin == 2 :
                    self.previous_wins["P2"] += 1
                self.active_round += 1
        
        elif self.active_round == 2:
            if status == True :   # active_round completed 
                if whoWin == 1 :
                    self.previous_wins["P1"] += 1
                elif whoWin == 2 :
                    self.previous_wins["P2"] += 1
                elif whoWin == 3:
                    if self.previous_wins["P1"] == 1:
                        self.previous_wins["P2"] = 1
                    else:
                        self.previous_health["P1"] = 1
                self.active_round += 1

        
        elif self.active_round == 3:
            if status == True :   # active_round completed 
                if whoWin == 1 :
                    self.previous_wins["P1"] += 1
                elif whoWin == 2 :
                    self.previous_wins["P2"] += 1
        
        # If current round is done get rewards pos/negatve 
        if status and (self.previous_wins["P1"] == 1 or self.previous_health["P2"] == 1):
            if whoWin == 1:
                data = add_rewards_constant(data,ROUND_BONUS)
            elif whoWin == 2:
                data = add_rewards_constant(data,-ROUND_BONUS)
        elif status and (self.previous_wins["P1"] == 2 or self.previous_health["P2"] == 2):
            if whoWin == 1:
                data = add_rewards_constant(data,self.stage*STAGE_BONUS)
            elif whoWin == 2:
                data = add_rewards_constant(data,-self.stage*STAGE_BONUS)

        # Game / Round / Stage done checks
        if (self.previous_wins["P1"] == 1 or self.previous_wins["P2"] == 1.0) and status :
            self.round_done = True         

        elif self.previous_wins["P1"] == 2:
            self.stage_done = True
            self.stage += 1
            # bu round done related to r not this.? spesific handle.self.round_done = True
        elif self.previous_wins["P2"] == 2:
            self.game_done = True
        
    
        return data

    # Collects the specified amount of frames the agent requires before choosing an action
    def gather_frames(self, actions):
        data = self.sub_step(actions)
        frames = [data["frame"]]
        for i in range(self.frames_per_step - 1):
            data = add_rewards(data, self.sub_step(actions))
            frames.append(data["frame"])
        data["frame"] = frames[0] if self.frames_per_step == 1 else frames
        return data

    # Steps the emulator along by one time step and feeds in any actions that require pressing
    # Takes the data returned from the step and updates book keeping variables
    def sub_step(self, actions):
        data = self.emu.step([action.value for action in actions])
        current_health = health_calculation(data["frame"],self.fullHP_p1,self.fullHP_p2)
        p1_diff = (self.previous_health["P1"] - current_health["P1"])
        p2_diff = (self.previous_health["P2"] - current_health["P2"])
        #print(current_health)
        self.previous_health = {"P1": current_health["P1"], "P2": current_health["P2"]}

        rewards = {
            "P1": (p2_diff-p1_diff),
            "P2": (p1_diff-p2_diff)
        }

        data["rewards"] = rewards
        return data

    # Steps the emulator along by the requested amount of frames required for the agent to provide actions
    def step(self, move_action, attack_action):
        if self.started:
            if not self.round_done and not self.stage_done and not self.game_done:
                actions = []
                actions += index_to_move_action(move_action)
                actions += index_to_attack_action(attack_action)
                data = self.gather_frames(actions)
                data = self.check_done(data)
                return data["frame"], data["rewards"], self.round_done, self.stage_done, self.game_done
            else:
                raise EnvironmentError("Attempted to step while characters are not fighting")
        else:
            raise EnvironmentError("Start must be called before stepping")


    # Safely closes emulator
    def close(self):
        self.emu.close()
