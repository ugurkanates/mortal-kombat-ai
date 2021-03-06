from PIL import Image, ImageChops
import numpy as np
import math
import operator
import os
import cv2 
path = os.getcwd()
print(path)
timer = (181, 6, 208, 25)  # thanks ImageMagics for pixel coordinates
P1_health_box = (20, 30, 182, 40)
P2_health_box = (207, 30, 368, 40)
crop_timer_img = (Image.open(path+"/assets/timer.png"))
crop_timer_img = crop_timer_img.convert("RGB")
win_icon = (Image.open(path+"/assets/win_icon.png"))
win_icon_img = win_icon.convert("RGB")
win_icon_sim_ratio = 0.88
win_icon_img_cv2 = cv2.imread(path+"/assets/min.png")
P1_LEFT = (25, 45, 35, 55)
P1_RIGHT = (35, 45, 45, 55)
P2_LEFT = (350, 45, 360, 55)
P2_RIGHT = (360, 45, 370, 55)
OpenCV = True

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

def rmsdiffer(liste):
    """Calculates the root mean square error (RSME) between two images"""
    # print(im1 , im2)
    # im1.show()
    # im2.show()
    errors = np.asarray(ImageChops.difference(liste[0], liste[1])) / 255
    x=  math.sqrt(np.mean(np.square(errors)))
    #print(x)
    return x

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
# PIL image input and output
def imgRemoveUtil(img1,img2):
    re1 = Image.fromarray(np.asarray(img1)- np.asarray(img1)) 
    re2 = Image.fromarray(np.asarray(img1)-np.asarray(img2))
    return re1,re2
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
def third_mean(which,frame):
    x = list()
    x = np.array(x)
    # p1 left, p1 right , p2 right , p2 left 
    if which == 1:    
        for i in range(len(frame)):
            res = cv2.cvtColor(frame[i],cv2.COLOR_RGB2BGR)
            res = res[45:55,25:35]
            x = np.append(x,cv2.matchTemplate(res,win_icon_img_cv2,cv2.TM_CCORR_NORMED).mean())
    elif which == 2:
        for i in range(len(frame)):
            res = cv2.cvtColor(frame[i],cv2.COLOR_RGB2BGR)
            res = res[45:55,35:45]
            x = np.append(x,cv2.matchTemplate(res,win_icon_img_cv2,cv2.TM_CCORR_NORMED).mean())
    elif which == 3:
        for i in range(len(frame)):
            res = cv2.cvtColor(frame[i],cv2.COLOR_RGB2BGR)
            res = res[45:55,360:370]
            x = np.append(x,cv2.matchTemplate(res,win_icon_img_cv2,cv2.TM_CCORR_NORMED).mean())
    elif which == 4:
        for i in range(len(frame)):
            res = cv2.cvtColor(frame[i],cv2.COLOR_RGB2BGR)
            res = res[45:55,350:360]
            x = np.append(x,cv2.matchTemplate(res,win_icon_img_cv2,cv2.TM_CCORR_NORMED).mean())
    
    return x.mean()


FRAME3 = True
def checkRoundDone(frame, currentRound):
     # Output = status,whoWin
     
    if OpenCV  == False:
        P1_R = Image.fromarray(frame, mode="RGB").crop(P1_RIGHT)
        P1_L = Image.fromarray(frame, mode="RGB").crop(P1_LEFT)
        P2_R = Image.fromarray(frame, mode="RGB").crop(P2_RIGHT)
        P2_L = Image.fromarray(frame, mode="RGB").crop(P2_LEFT)
        status = False
        whoWin = -1
        if currentRound == 1:
            # Left L  - Right R
            if rmsdiffer(imgRemoveUtil(P1_L, win_icon_img)) < win_icon_sim_ratio:
                #P1_L.save("ucan.png")
                #win_icon_img.save("hadi.png")
                print("Left Round 1 Won")
                status = True
                whoWin = 1
            elif rmsdiffer(imgRemoveUtil(P2_R,win_icon_img)) < win_icon_sim_ratio:
                print("Right Round 1 Won")
                status = True
                whoWin = 2
            #else:
            #   print("none?")
        elif currentRound == 2:
            # Left Win yaparsa stage_done  or beraber
            # Right win yaparsa either beraber or game done
            # LL bakmak lazim round1i kaybettiysek
            # LR bakmak lazim round1'i kazandiysak
            # RL , RR again.
            # 1- LR -RL durumunda whoWin 3 yolla disarda kontrol etsin
            # diger grumlar aynı
            if (rmsdiffer(imgRemoveUtil(P1_L,win_icon_img)) < win_icon_sim_ratio and \
                rmsdiffer(imgRemoveUtil(P2_R,win_icon_img)) < win_icon_sim_ratio  ):
                print("WHAfaknigger")
                status = True
                whoWin = 3
            elif rmsdiffer(imgRemoveUtil(P1_R,win_icon_img)) < win_icon_sim_ratio:     
                print("Left side won somehow.")
                print(rmsdiffe(P1_R,win_icon_img))
                P1_R.show()
                status = True
                whoWin = 1
            elif rmsdiffer(imgRemoveUtil(P2_L,win_icon_img)) < win_icon_sim_ratio:
                print("Right side won somehow.")
                status = True
                whoWin = 2

        elif currentRound == 3:
            # Check LR  and RL
            if rmsdiffer(imgRemoveUtil(P1_R,win_icon_img)) < win_icon_sim_ratio:
                status = True
                whoWin = 1
            elif rmsdiffer(imgRemoveUtil(P2_L,win_icon_img)) <win_icon_sim_ratio:
                status = True
                whoWin = 2
    elif FRAME3 == True:

        status = False
        whoWin = -1
        if currentRound == 1:
            # Left L  - Right R
            #if rmsdiffer(imgRemoveUtil(P1_L, win_icon_img)) < win_icon_sim_ratio:
            if third_mean(1,frame) > win_icon_sim_ratio:
                #P1_L.save("ucan.png")
                #win_icon_img.save("hadi.png")
                print("Left Round 1 Won")
                #print(cv2.matchTemplate(P1_L,win_icon_img_cv2,cv2.TM_CCORR_NORMED).mean())
                #cv2.imwrite("neymis.png",P1_L)
                status = True
                whoWin = 1
            #elif rmsdiffer(imgRemoveUtil(P2_R,win_icon_img)) < win_icon_sim_ratio:
            elif third_mean(3,frame)> win_icon_sim_ratio:
                print("Right Round 1 Won")
                status = True
                whoWin = 2

        elif currentRound == 2:
            # Left Win yaparsa stage_done  or beraber
            # Right win yaparsa either beraber or game done
            # LL bakmak lazim round1i kaybettiysek
            # LR bakmak lazim round1'i kazandiysak
            # RL , RR again.
            # 1- LR -RL durumunda whoWin 3 yolla disarda kontrol etsin
            # diger grumlar aynı
            if third_mean(1,frame) > win_icon_sim_ratio and \
                third_mean(3,frame) > win_icon_sim_ratio:
                print("WHAfaknigger")
                status = True
                whoWin = 3
            #elif rmsdiffer(imgRemoveUtil(P1_R,win_icon_img)) < win_icon_sim_ratio: 
            elif third_mean(2,frame) > win_icon_sim_ratio:    
                print("Left side won somehow.")
                #cv2.imwrite("neymis.png",P1_R)
                #print(cv2.matchTemplate(P1_R,win_icon_img_cv2,cv2.TM_CCORR_NORMED).mean())
                #print(rmsdiffe(P1_R,win_icon_img))
                #P1_R.show()
                status = True
                whoWin = 1
            #elif rmsdiffer(imgRemoveUtil(P2_L,win_icon_img)) < win_icon_sim_ratio:
            elif third_mean(4,frame) > win_icon_sim_ratio:
                print("Right side won somehow.")
                status = True
                whoWin = 2


        elif currentRound == 3:
            # Check LR  and RL
            if third_mean(2,frame) > win_icon_sim_ratio:
            #if rmsdiffer(imgRemoveUtil(P1_R,win_icon_img)) < win_icon_sim_ratio:
                status = True
                whoWin = 1
            #elif rmsdiffer(imgRemoveUtil(P2_L,win_icon_img)) <win_icon_sim_ratio:
            elif third_mean(4,frame) > win_icon_sim_ratio:

                status = True
                whoWin = 2


    else:
        frame = cv2.cvtColor(frame,cv2.COLOR_RGB2BGR)
        P1_R = frame[45:55,35:45]
        P1_L = frame[45:55,25:35]
        P2_R = frame[45:55,360:370]
        P2_L = frame[45:55,350:360]
        status = False
        whoWin = -1
        if currentRound == 1:
            # Left L  - Right R
            #if rmsdiffer(imgRemoveUtil(P1_L, win_icon_img)) < win_icon_sim_ratio:
            if cv2.matchTemplate(P1_L,win_icon_img_cv2,cv2.TM_CCORR_NORMED).mean() > win_icon_sim_ratio:
                #P1_L.save("ucan.png")
                #win_icon_img.save("hadi.png")
                print("Left Round 1 Won")
                print(cv2.matchTemplate(P1_L,win_icon_img_cv2,cv2.TM_CCORR_NORMED).mean())
                cv2.imwrite("neymis.png",P1_L)
                status = True
                whoWin = 1
            #elif rmsdiffer(imgRemoveUtil(P2_R,win_icon_img)) < win_icon_sim_ratio:
            elif cv2.matchTemplate(P2_R,win_icon_img_cv2,cv2.TM_CCORR_NORMED).mean()> win_icon_sim_ratio:
                print("Right Round 1 Won")
                status = True
                whoWin = 2
            #else:
            #   print("none?")
        elif currentRound == 2:
            # Left Win yaparsa stage_done  or beraber
            # Right win yaparsa either beraber or game done
            # LL bakmak lazim round1i kaybettiysek
            # LR bakmak lazim round1'i kazandiysak
            # RL , RR again.
            # 1- LR -RL durumunda whoWin 3 yolla disarda kontrol etsin
            # diger grumlar aynı
            if (cv2.matchTemplate(P1_L,win_icon_img_cv2,cv2.TM_CCORR_NORMED).mean()> win_icon_sim_ratio and \
                cv2.matchTemplate(P2_R,win_icon_img_cv2,cv2.TM_CCORR_NORMED).mean() > win_icon_sim_ratio):

            #if (rmsdiffer(imgRemoveUtil(P1_L,win_icon_img)) < win_icon_sim_ratio and \
             #   rmsdiffer(imgRemoveUtil(P2_R,win_icon_img)) < win_icon_sim_ratio  ):
                print("WHAfaknigger")
                status = True
                whoWin = 3
            #elif rmsdiffer(imgRemoveUtil(P1_R,win_icon_img)) < win_icon_sim_ratio: 
            elif cv2.matchTemplate(P1_R,win_icon_img_cv2,cv2.TM_CCORR_NORMED).mean() > win_icon_sim_ratio:    
                print("Left side won somehow.")
                cv2.imwrite("neymis.png",P1_R)
                print(cv2.matchTemplate(P1_R,win_icon_img_cv2,cv2.TM_CCORR_NORMED).mean())
                #print(rmsdiffe(P1_R,win_icon_img))
                #P1_R.show()
                status = True
                whoWin = 1
            #elif rmsdiffer(imgRemoveUtil(P2_L,win_icon_img)) < win_icon_sim_ratio:
            elif cv2.matchTemplate(P2_L,win_icon_img_cv2,cv2.TM_CCORR_NORMED).mean() > win_icon_sim_ratio:
                print("Right side won somehow.")
                status = True
                whoWin = 2


        elif currentRound == 3:
            # Check LR  and RL
            if cv2.matchTemplate(P1_R,win_icon_img_cv2,cv2.TM_CCORR_NORMED).mean() > win_icon_sim_ratio:
            #if rmsdiffer(imgRemoveUtil(P1_R,win_icon_img)) < win_icon_sim_ratio:
                status = True
                whoWin = 1
            #elif rmsdiffer(imgRemoveUtil(P2_L,win_icon_img)) <win_icon_sim_ratio:
            elif cv2.matchTemplate(P2_L,win_icon_img_cv2,cv2.TM_CCORR_NORMED).mean() > win_icon_sim_ratio:

                status = True
                whoWin = 2

    return status,whoWin


