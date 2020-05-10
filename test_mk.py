import random
from mk_environment import Environment
from PIL import Image

roms_path = "roms"  # Replace this with the path to your ROMs
game_id = "mk"
shoots_folder = "screens/"
env = Environment("env1", roms_path,game_id,throttle=True,frame_ratio=1)
P1_dim = (20,30,182,40)

for i in range(100):
    data = env.gather_frames([])
    img = Image.fromarray(data['frame'][0],'RGB')
    imCut = img.crop(P1_dim)
    imCut.save(shoots_folder+str(i)+".png")
print("1")
#env.start()
"""
    frames, reward, round_done, stage_done, game_done = env.step(move_action, attack_action)
    if game_done:
        env.new_game()
    elif stage_done:
        env.next_stage()
    elif round_done:
        env.next_round()
"""