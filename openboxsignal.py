import cv2
import numpy as np
import PIL
from PIL import Image
from djitellopy import tello
import time

start = time.time()
me = tello.Tello()
me.connect()
print(me.get_battery())
me.streamon()
prbr = [None]*3 #previous brightness
absdif = [0] #absolue difference between prev and current brightness
h = [0] #just a constant

frameWidth = 640
frameHeight = 480
#cap = me.get_frame_read() #cv2.VideoCapture(0)
#cap.set(3, frameWidth)
#cap.set(4, frameHeight)
start = time.time()

def brightness(im_file):
    im = im_file#cv2.cvtColor(im_file,cv2.COLOR_BGR2GRAY)
    avg = cv2.mean(im)
    #stat = PIL.ImageStat.Stat(im, mask=None)
    return avg #stat.mean[0]
while True:
    cap = me.get_frame_read().frame
    img = cap
    img = cv2.resize(img, (360,240))
    #_, img = cap.read()
    if time.time()-start > 2:
        for i in range(3):
            try:
                absdif[0] += abs(prbr[i]-brightness(img)[i])
            except: pass
        if absdif[0] < 15:
            for i in range(3):
                prbr[i]=brightness(img)[i]

        print(brightness(img))
        print("absdif = "+str(absdif[0]))
        if absdif[0] >= 15:
            h[0] += 1
        else:
            h[0] = 0
        if h[0]>=20:
            break
        absdif[0]=0
        print("h[0] = "+str(h[0]))
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            break

me.streamoff()
