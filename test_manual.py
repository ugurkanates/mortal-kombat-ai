import random
from mk_environment import Environment
from MAMEToolkit.emulator import run_cheat_debugger

roms_path = "roms"  # Replace this with the path to your ROMs
game_id = "mk"

from MAMEToolkit import emulator
env = Environment("env1", roms_path,game_id,throttle=False,frame_ratio=3,character="SONYA")
env.start()
for i in range(1000):
    result = env.step(1,1)
    if result[2] == True:
        env.round_done = False
        print("Round done? doubt")
        env.wait_for_fight_start()
    elif result[3] == True:
        print("aq")
    elif result[4] == True:
        env.game_done = False
        print("Game lost, restarting it.")
        env.startAfterFail()
    #print(x[2],x[4],x[4])
#run_cheat_debugger(roms_path, game_id,binary_path="/home/paypaytr/Desktop/ReinforcementLearning/mame_compile/mame/mamearcade64")
