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
    
    retL, cornersL = cv.findChessboardCorners(imgL, (8,6), None)
    retR, cornersR = cv.findChessboardCorners(imgR, (8,6), None)
    
    # print("hello world")
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
# ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

# #Plot undistorted 
# h,  w = img.shape[:2]
# newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))

# dst = cv.undistort(img, mtx, dist, None, newcameramtx)
# # crop the image
# x, y, w, h = roi
# dst = dst[y:y+h, x:x+w]
# plt.figure()
# plt.imshow(dst)
# plt.savefig("undistorted.png", dpi = 300)
# plt.close()