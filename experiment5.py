import time
from time import sleep
import matplotlib.pyplot as plt
t0 = []
t1 = []
expve = []
actve = []
zposs = []
xposs = []
yposs = []
n=579-1 #number of lines -1
''' actv not needed for now
for i in range(0, n, 100):
    time0 = open("time0.txt", "r")
    t0.append(float(time0.readlines()[i]))
    time0.close()
    actv = open("actv.txt", "r")
    actve.append(float(actv.readlines()[i]))
    actv.close()
for i in range(n):
    time1= open("time1.txt", "r")
    t1.append(float(time1.readlines()[i]))
    time1.close()
    expv = open("expv.txt", "r")
    expve.append(float(expv.readlines()[i]))
    expv.close()
'''
for i in range(n):
    time1= open("time1.txt", "r")
    t1.append(float(time1.readlines()[i+1]))
    time1.close()
    zpostxt = open("zpos.txt", "r")
    zposs.append(float(zpostxt.readlines()[i+1]))
    zpostxt.close()
    xpostxt = open("xpos.txt", "r")
    xposs.append(float(xpostxt.readlines()[i+1]))
    xpostxt.close()
    ypostxt = open("ypos.txt", "r")
    yposs.append(float(ypostxt.readlines()[i+1]))
    ypostxt.close()

#plt.plot(t0,actve)
#plt.plot(t1,expve)
plt.plot(t1, zposs)
plt.plot(t1, xposs)
plt.plot(t1, yposs)
plt.title("Blue - z, Orange - x, Green - y")
plt.show()