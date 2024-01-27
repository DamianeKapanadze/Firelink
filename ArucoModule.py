import cv2
import cv2.aruco as aruco
import numpy as np
import os

def findarucomarkers(img, markerSize=6, totalMarkers=250, draw=True):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    key = getattr(aruco, f'DICT_{markerSize}X{markerSize}_{totalMarkers}')
    arucoDict = aruco.Dictionary_get(key)
    arucoParam = aruco.DetectorParameters_create()
    bboxs, ids, rejected = aruco.detectMarkers(imgGray, arucoDict, parameters=arucoParam)
    print(bboxs)
    if draw:
        aruco.drawDetectedMarkers(img, bboxs)

coordinates = []
def main():
    cap = cv2.VideoCapture(0)

    while True:
        success, img = cap.read()
        coordinates.append(findarucomarkers(img))
        print(coordinates[0])
        #rectangle(img)
        cv2.imshow("Image", img)
        cv2.waitKey(1)

def rectangle(img):
    imgGray = cv2.cvtcolor(img, cv2.COLOR_BGR2GRAY)
    for(x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)
if __name__ == "__main__":
    main()


#calculate size of aruco: https://arshren.medium.com/measure-object-size-using-opencv-and-aruco-marker-fa8b2e3b0572