import random
from mk_environment import Environment

roms_path = "roms"  # Replace this with the path to your ROMs
game_id = "mk"
env = Environment("env1", roms_path,game_id)
#env.start()
"""while True:
    move_action = random.randint(0, 8)
    attack_action = random.randint(0, 9)
    frames, reward, round_done, stage_done, game_done = env.step(move_action, attack_action)
    if game_done:
        env.new_game()
    elif stage_done:
        env.next_stage()
    elif round_done:
        env.next_round()
"""