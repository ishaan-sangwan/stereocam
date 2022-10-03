from unittest.mock import CallableMixin
import numpy as np
import cv2 as cv
import glob
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

chessboardSize = (6,9)
frameSize = (640, 480)

#termination criteria
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

objp = np.zeros((chessboardSize[0]*chessboardSize[1],3), np.float32)
objp[:,:2] = np.mgrid[0:chessboardSize[0],0:chessboardSize[1]].T.reshape(-1,2)
flags = cv.CALIB_CB_NORMALIZE_IMAGE | cv.CALIB_CB_EXHAUSTIVE | cv.CALIB_CB_ACCURACY


objp = objp*20

objpoints = []
imgpointsL = []
imgpointsR = []

imagesLeft = glob.glob('images/stereoLeft/*.png')
imagesRight = glob.glob("images/stereoRight/*.png")
# print(imgpointsL)
# print("hello")
num = 0
for imgLeft,imgRight in zip(imagesLeft,imagesRight):
    imgL = cv.imread(imgLeft)
    imgR = cv.imread(imgRight)
    
    grayL = cv.cvtColor(imgL, cv.COLOR_BGR2GRAY)
    grayR = cv.cvtColor(imgR, cv.COLOR_BGR2GRAY)
    
    retL, cornersL = cv.findChessboardCorners(imgL, (8,6), None, flags=flags)
    retR, cornersR = cv.findChessboardCorners(imgR, (8,6), None, flags=flags)
    
    print(retL)
    if retL and retR==True:
        objpoints.append(objp)
        
        cornersL = cv.cornerSubPix(grayL,np.float32(cornersL), (11,11), (-1,-1),criteria)
        imgpointsL.append(cornersL)
        cornersR = cv.cornerSubPix(grayR, np.float32(cornersR), (11,11), (-1,-1), criteria)
        imgpointsR.append(cornersR)
        
        cv.drawChessboardCorners(imgL, chessboardSize, cornersL, retL)
        cv.imshow("img left",imgL)
        # cv.imwrite("images/final/"+str(num)+".png", imgL)
        cv.drawChessboardCorners(imgR, chessboardSize, cornersR, retR)
        cv.imshow("img right",imgR)
    
        # num+=1
        
        cv.waitKey(10000)
cv.destroyAllWindows()

#------------------------------------

retL , cameraMatrixL, distL, rvsecsL,tvecsL =cv.calibrateCamera(objpoints, imgpointsL,frameSize, None,None)
heightL, widthL, channelsL = imgL.shape
newCameraMatrixL, roi_L = cv.getOptimalNewCameraMatrix(cameraMatrixL, distL,(widthL, heightL),1,(widthL, heightL))

retR, cameraMatrixR, distR, rvsecsR, tvecsR = cv.calibrateCamera(objpoints, imgpointsR, frameSize, None, None)
heightR, widthR, channelsR = imgR.shape
newCameraMatrixR, roi_R = cv.getOptimalNewCameraMatrix(cameraMatrixR, distR, (widthR, heightR), 1,None, None)

#------------------------------------

flags = 0
flags|=cv.CALIB_FIX_INTRINSIC


criteria_stereo = (cv.TERM_CRITERIA_EPS +cv.TERM_CRITERIA_MAX_ITER,30,0.001)
# retStereo,newCameraMatrixL, distL, newCameraMatrixR, distR, rot,trans,essentialMatrix, fundamentalMatrix=
#----------------------------------

rectifyScale = 1
rectL, rectR, projMatrixL, projMatrixR, Q, roi_L, roi_R = cv.stereoRectify(newCameraMatrixL, distL,newCameraMatrixR, distR, grayL, grayR)
stereomapL = cv.initUndistortRectifyMap(newCameraMatrixL, distL, rectL, projMatrixL, grayL.shape[::-1], cv.CV_16SC2)
stereomapR = cv.initUndistortRectifyMap(newCameraMatrixR, distL, rectL, projMatrixR, grayR.shape[::-1], cv.CV_16SC2)

print("saving parameters!")

cv_file = cv.FileStorage("stereomap.xml", cv.FILE_STORAGE_WRITE)

cv_file.write("stereoMapL_x", stereomapL[0])
cv_file.write("stereoMapL_y", stereomapL[1])
cv_file.write("stereoMapR_x", stereomapR[0])
cv_file.write("stereoMapR_y", stereomapR[1])

cv_file.release()