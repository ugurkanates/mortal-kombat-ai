import random
from mk_environment import Environment
from MAMEToolkit.emulator import run_cheat_debugger

roms_path = "roms"  # Replace this with the path to your ROMs
game_id = "mk"

from MAMEToolkit import emulator
env = Environment("env1", roms_path,game_id,throttle=True,frame_ratio=1,character="RAIDEN")
env.start()
#run_cheat_debugger(roms_path, game_id,binary_path="/home/paypaytr/Desktop/ReinforcementLearning/mame_compile/mame/mamearcade64")
