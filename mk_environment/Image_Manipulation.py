from PIL import Image, ImageChops
import numpy as np
import math
import operator
import os
path = os.getcwd()
print(path)
timer = (181, 6, 208, 25)  # thanks ImageMagics for pixel coordinates
P1_health_box = (20, 30, 182, 40)
P2_health_box = (207, 30, 368, 40)
crop_timer_img = (Image.open(path+"/assets/timer.png"))
crop_timer_img = crop_timer_img.convert("RGB")
win_icon = (Image.open(path+"/assets/win_icon.png"))
win_icon_img = win_icon.convert("RGB")
win_icon_sim_ratio = 0.415
P1_LEFT = (25, 45, 35, 55)
P1_RIGHT = (35, 45, 45, 55)
P2_LEFT = (350, 45, 360, 55)
P2_RIGHT = (360, 45, 370, 55)

# from single image returns PIL type cropped timer for comparison
# if fight started etc


def crop_timer(imge):
    imge = Image.fromarray(imge, mode="RGB")
    imge = imge.crop(timer)
    return imge

# its a very naive approach but I found it's working so why not
# anything else would be improement , histogram based ones etc
# or teaching OCR network like tesseract for mame fonts
# but didn't have time for it so its basic pixel comparison cheers :D
# returns their difference so 1- output will be how similiar they are.


def rmsdiffe(im1, im2):
    """Calculates the root mean square error (RSME) between two images"""
    # print(im1 , im2)
    # im1.show()
    # im2.show()
    errors = np.asarray(ImageChops.difference(im1, im2)) / 255
    return math.sqrt(np.mean(np.square(errors)))

# integer argument , gets of health bar of p1 or p2 1,2 arguments


def get_health_bar(frame, which):
    if which == 1:
        imge = Image.fromarray(frame, mode="RGB")
        return imge.crop(P1_health_box)
    elif which == 2:
        imge = Image.fromarray(frame, mode="RGB")
        return imge.crop(P2_health_box)
    else:
        print("big ERROR HEALTH BAR wrong argm")
        return 0


def health_calculation(frame, p1, p2):

    # Full Image to check on
    p1_full = Image.fromarray(np.asarray(p1)-np.asarray(p1))
    # Full Image to check on
    p2_full = Image.fromarray(np.asarray(p2)-np.asarray(p2))

    part_p1 = get_health_bar(frame, 1)
    part_p1 = Image.fromarray(np.asarray(p1)-np.asarray(part_p1))

    part_p2 = get_health_bar(frame, 2)
    part_p2 = Image.fromarray(np.asarray(p2)-np.asarray(part_p2))

    x = 1 - rmsdiffe(p1_full, part_p1)
    y = 1 - rmsdiffe(p2_full, part_p2)
    return {"P1": x, "P2": y}


def checkRoundDone(frame, currentRound):
     # Output = status,whoWin
     P1_R = Image.fromarray(frame, mode="RGB").crop(P1_RIGHT)
     P1_L = Image.fromarray(frame, mode="RGB").crop(P1_LEFT)
     P2_R = Image.fromarray(frame, mode="RGB").crop(P2_RIGHT)
     P2_L = Image.fromarray(frame, mode="RGB").crop(P2_LEFT)
     status = False
     whoWin = -1
     if currentRound == 1:
        # Left L  - Right R
        if rmsdiffe(P1_L, win_icon_img) < win_icon_sim_ratio:
             P1_L.save("ucan.png")
             win_icon_img.save("hadi.png")
             print("Left Round 1 Won")
             status = True
             whoWin = 1
        elif rmsdiffe(P1_R,win_icon_img) < win_icon_sim_ratio:
            print("Right Round 1 Won")
            status = True
            whoWin = 2
        else:
            print("none?")
     elif currentRound == 2:
         # Left Win yaparsa stage_done  or beraber
         # Right win yaparsa either beraber or game done
         # LL bakmak lazim round1i kaybettiysek
         # LR bakmak lazim round1'i kazandiysak
         # RL , RR again.

        if rmsdiffe(P1_L,win_icon_img) < win_icon_sim_ratio or rmsdiffe(P1_R,win_icon_img) < win_icon_sim_ratio:
            print("Left side won somehow.")
            status = True
            whoWin = 1
        elif rmsdiffe(P2_R,win_icon_img) < win_icon_sim_ratio or rmsdiffe(P2_L,win_icon_img) < win_icon_sim_ratio:
            print("Right side won somehow.")
            status = True
            whoWin = 2

     elif currentRound == 3:
         # Check LR  and RL
        if rmsdiffe(P1_R,win_icon_img) < win_icon_sim_ratio:
            status = True
            whoWin = 1
        elif rmsdiffe(P2_L,win_icon_img) <win_icon_sim_ratio:
            status = True
            whoWin = 2
     return status,whoWin

