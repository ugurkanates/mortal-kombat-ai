import random
from mk_environment import Environment
from MAMEToolkit.emulator import run_cheat_debugger

roms_path = "roms"  # Replace this with the path to your ROMs
game_id = "mk"

from MAMEToolkit import emulator
emu = emulator.Emulator("env_id", roms_path,game_id,0,frame_ratio=3) #throttle=True)
emu.start()
#run_cheat_debugger(roms_path, game_id,binary_path="/home/paypaytr/Desktop/ReinforcementLearning/mame_compile/mame/mamearcade64")
