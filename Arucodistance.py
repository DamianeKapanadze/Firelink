import cv2

dictionary = cv.aruco.Dictionary_get(cv.aruco.DICT_6X6_250)
parameters = cv.aruco.DetectorParameters_create()
#frame = my camera
(corners, ids, rejected) = cv.aruco.detectMarkers(frame, dictionary, parameters=parameters)
rvecaruco.estimatePoseSingleMarkers()
markerSizeInCM = 15.9 #aruco side length
rvec , tvec, _ = aruco.estimatePoseSingleMarkers(corners, markerSizeInCM, mtx, dist)
