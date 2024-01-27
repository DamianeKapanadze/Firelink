from djitellopy import tello
from ArucoModule import findarucomarkers
import cv2
import time
import numpy as np
import math
# import cameracalibration
import random
import KeyPressModule as kp
from time import sleep
import cv2.aruco as aruco
import pygame
#import matplotlib.pyplot as plt

XDDDDDD = False
x=None
num = [1]

r = [None]*4 #actual values of x, z, y, and yaw
v = [None]*4 #velocity
e = [None]*4 #expected change
d = [None]*4 #real changes in distances
p = [None]*4 #previous values
errv = [None]*4 #average error velocity
pvel = [None]*4 #previous velocities given so that same signal isnt sent many times
c = [0] #just useless constant for the end of the code. To see how many times aruco hasnt been seen in a row
checkpoint = [5]

time1txt = open("time1.txt", "w") #graph using experiment5.py
time1txt.write(str(0) + "\n")
time1txt.close()
xposstxt = open("xpos.txt", "w")
xposstxt.write(str(0) + "\n") #to clear the file
xposstxt.close()
zposstxt = open("zpos.txt", "w")
zposstxt.write(str(0) + "\n") #to clear the file
zposstxt.close()
yposstxt = open("ypos.txt", "w")
yposstxt.write(str(0) + "\n") #to clear the file
yposstxt.close()

start = time.time()
kp.init()
me = tello.Tello()
me.connect()
me.streamon()
sleep(0.5)
print(me.get_battery())
me.takeoff()
'''
goupvel = 20
goupvelt = (120-me.get_height())/goupvel
if goupvelt<0:
    goupvelt= -goupvelt
    goupvel = -goupvel
me.send_rc_control(0, 0, goupvel, 0)
sleep(goupvelt)
'''
me.send_rc_control(0,-30, 0, 0)
sleep(5)
'''
me.send_rc_control(10, 0, 0, 30)
sleep(12)
curyaw = me.get_yaw()
print("yaw = "+str(curyaw))
twait = 0
if curyaw>0:
    twait = (360-curyaw)/30
elif curyaw<0:
    twait = abs(curyaw)/30
me.send_rc_control(10, 0, 0, 30)
sleep(twait)
curyaw = me.get_yaw()
if curyaw > 0:
    me.rotate_counter_clockwise(int(curyaw))
else:
    me.rotate_clockwise(int(-curyaw))
sleep(2.5)
curyaw = me.get_yaw()
if curyaw > 0:
    me.rotate_counter_clockwise(int(curyaw))
else:
    me.rotate_clockwise(int(-curyaw))
sleep(2.5)
'''
#me.flip_forward()

me.send_rc_control(0,0,0,0)
# hait = me.get_height()
# heightofaruco = 0 #height of aruco from ground in cm
# mvupheight = 130-hait
# if hait<130:
#  me.move_up(mvupheight) #bring to desired hight so that it doesnt collide with things
# me.curve_xyz_speed(70, 70, 0, 20, 20, 0, 10) #make a curve and finish 20 cms offset on x,y, since searchforaruco() might collide otherwise


def getKeyboardInput():
    lr, fb, ud, yv = 0, 0, 0, 0
    speed = 50
    if kp.getKey("LEFT"):
        lr = -speed
    elif kp.getKey("RIGHT"):
        lr = speed
    if kp.getKey("UP"):
        fb = speed
    elif kp.getKey("DOWN"):
        fb = -speed
    if kp.getKey("w"):
        ud = speed
    elif kp.getKey("s"):
        ud = -speed
    if kp.getKey("a"):
        yv = -speed
    elif kp.getKey("d"):
        yv = speed
    if kp.getKey("q"):
        me.land()
        sleep(3)
    if kp.getKey("e"):
        me.takeoff()
    return [lr, fb, ud, yv]
def flyilia(x,y,z,pitch):
    #if lol == 1:
      #  me.send_rc_control(0, 0, 0, -10)
    #if z>80:
    #    z-=40
    #w = int(180/(math.pi)*math.atan(x/z))
    #num[0] = -num[0]
    '''
    if abs(w) > 10:  # 10cm is accepted deviation from target
        yawvel = int(0.8*w)
    else:
        yawvel = 0
    '''

    yawvel = 0
    xvel = 0
    if abs(x)<10:
        xvel = int(x)
    else:
        if x>0:
            xvel=10
        else:
            xvel=-10
    '''
    if abs(x) > 2: #see comment below
        if x>0:
            xvel = 7
        else:
            xvel = -7
     #this was movement for y, but i changed it cause it dont work 2 close
    if y > 30: #assumes y>0
        upvel = -10
    else:
        upvel = 0
    '''
    if z>150: #it was (z**2+x**2)>22500
        zvel = 15
    #elif 40<=z<=150:
    elif 45<=z<=150: #maybe 45
        zvel = 10
    else:
        zvel = 7
    #else: #previously, it was else: zvel=10
    #    zvel = int(z/4)
    if z<45:
        y +=17 #MAYBE TRY WITHOUT IT
    #y -=10 #so that drone flies 10 cm below it currently flies
    # desired y = - z * tan(pitch), since camera has a pitch angle
    if abs(y+z*math.tan(pitch))<20:
        if abs(y+z*math.tan(pitch))>0:
            upvel = int(-(y+z*math.tan(pitch))/2)
    else:
        if y+z*math.tan(pitch) > 0:
            upvel = -10
        else:
            upvel = 10
    upvel = int(upvel+zvel*math.tan(pitch))

    #zvel += num[0] #maybe delete this. tello.py response timeout can be changed
    xvel = int(xvel)
    upvel = int(upvel)
    zvel = int(zvel)
    #try:
    #    if pvel[0] != xvel or pvel[1] != zvel or pvel[2] != upvel:
    #        me.send_rc_control(xvel, zvel, upvel, yawvel)
    #except:
    me.send_rc_control(xvel, zvel, upvel, yawvel)
    ''' pvel[] is useless rn
    pvel[0] = xvel
    pvel[1] = zvel
    pvel[2] = upvel
    '''
    #if (z**2+x**2)<=580:
    if z<=22:
        me.send_rc_control(0,-3,0,0)
        global XDDDDDD
        XDDDDDD= True
        print(me.get_battery())
        me.land()
        print("total time = "+str(time.time()-start))



# define Tag
id_to_find = 26
marker_size = 4.9  # cm, needs to be measured

# get camera calibration path
calib_path = ""
camera_martix = np.loadtxt(calib_path + 'cameraMatrix.txt', delimiter=',')
camera_distortion = np.loadtxt(calib_path + 'cameraDistortion.txt', delimiter=',')

# 180 degree rotation matrix around x-axis
R_flip = np.zeros((3, 3), dtype=np.float32)
R_flip[0, 0] = 1.0
R_flip[1, 1] = -1.0
R_flip[2, 2] = -1.0

# define aruco dictionary
aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
parameters = aruco.DetectorParameters_create()

# font for text
font = cv2.FONT_HERSHEY_PLAIN

while True:
    # capture video
    cap = me.get_video_capture()
    # cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 360)  # 1280) #maybe change to 360
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)  # 720) #maybe change to 240

    ret, frame = cap.read()  # read frames
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # convert to gray img
    corners, ids, rejected = aruco.detectMarkers(image=gray, dictionary=aruco_dict,
                                                 parameters=parameters)  # , cameraMatrix = camera_martix, distCoeff= camera_distortion) #detect arucos
    if ids != None and ids[0] == id_to_find:
        # ret = [rvec, tvec, ?]
        # array of rotation and position of each marker (1 in our case)
        ret = aruco.estimatePoseSingleMarkers(corners, marker_size, camera_martix, camera_distortion)
        # we only need 1st
        rvec, tvec = ret[0][0, 0, :], ret[1][0, 0, :]
        try:
            for i in range(4):
                print("rvec["+str(i)+"] = "+str(rvec[i]))
        except: pass
        # draw

        # aruco.drawDetectedMarkers(frame, corners)

        # aruco.drawAxis(frame, camera_martix, camera_distortion, rvec, tvec, 10) #it doesnt work 4 som rison

        # write position

        # str_position = "Marker Position x=%4.0f  y=%4.0f  z=%4.0f" % (tvec[0], tvec[1], tvec[2])
        # cv2.putText(frame, str_position, (0, 100), font, 1, (0, 0, 255), 2, cv2.LINE_AA)

    # display

    # cv2.imshow("frame", frame)

    # use q to quit
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        break
    try:
        if x!=tvec[0] and tvec[0]!= None:
            lol0 = 0
        else:
            lol0=1
        x = tvec[0]
        y = tvec[1]
        z = tvec[2]
        pitch = math.pi*(me.get_pitch()-17)/180
        z0 = z
        y0 = y
        z = z0*math.cos(pitch)+y0*math.sin(pitch)
        y = y0*math.cos(pitch)-z0*math.sin(pitch)
        print("x = "+str(x))
        print("y = " + str(y))
        print("y0 = " + str(y0))
        print("z = " + str(z))
        print("z0 = " + str(z0))
        print("pitch = " + str(me.get_pitch()))
        lol = lol0
    except:
        lol = 1
        print("Error")
    print("lol = "+str(lol))
    '''
    try:
        if z>200:
            sleep(0.5)
        elif 200>=z>130:
            sleep(0.05)
    except: pass
    '''
    try:
        print("c[0] = "+str(c[0]))
    except: pass
    if lol == 0:
        print("fly ilia is on")
        try:
            time1txt = open("time1.txt", "a")
            time1txt.write(str(time.time()-start) + "\n")  # time
            time1txt.close()
            zposstxt = open("zpos.txt", "a")
            zposstxt.write(str(z) + "\n")  # z
            zposstxt.close()
            yposstxt = open("ypos.txt", "a")
            yposstxt.write(str(y) + "\n")  # y
            yposstxt.close()
            xposstxt = open("xpos.txt", "a")
            xposstxt.write(str(x) + "\n")  # x
            xposstxt.close()
        except: pass
        c[0]=0
        flyilia(x, y, z, pitch) #pitch is for vertical corrections
    if XDDDDDD:
        print("broken")
        me.streamoff()
        break
    elif kp.getKey("9"):
        me.land()
        me.streamoff()
        break
    try:
        if lol==1 and z>0:
            c[0]+=1
        if 2 <=c[0] <= 15:
            me.send_rc_control(0,0,0,0)
        elif 500>c[0]>15:
            print("cudad aris saqme megobrebo")
            if abs(x)>abs(y):
                if z>45:
                    if x>0:
                        me.send_rc_control(10, 0,0,0)
                    elif x<0:
                        me.send_rc_control(-10,0,0,0)
                else:
                    if x>0:
                        me.send_rc_control(10, -10,0,0)
                    elif x<0:
                        me.send_rc_control(-10, -10,0,0)
            else:
                if z>45:
                    me.send_rc_control(0, 0, -10, 0)
                else:
                    me.send_rc_control(0, -5, -15, 0)
        elif c[0]>=500:
            print("dzalian cudad aris saqme megobrebo")
            if abs(x) > abs(y):
                if x > 0:
                    me.send_rc_control(10, -10, 0, 0)
                elif x < 0:
                    me.send_rc_control(-10, -10, 0, 0)
            elif me.get_height()>20: #me.getehight can be printed 3 cheq
                me.send_rc_control(0, -10, -10, 0)
            elif me.get_height()<=20:
                me.send_rc_control(0, 0, 10, 0)
                sleep(1.5)
                y=0
    except: pass

