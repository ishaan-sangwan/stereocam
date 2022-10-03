import cv2

cam1 = cv2.VideoCapture(0)
cam2 = cv2.VideoCapture(1)
# cam1.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
# cam2.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
num =0

while cam1.isOpened():
    ret1, img1 = cam1.read()
    ret2, img2 = cam2.read()
    img1 = cv2.flip(img1, 1)
    
    if ret1:
        cv2.imshow("img1", img1)
    if ret2:
        cv2.imshow("img2", img2)
        
    # im_h = cv2.hconcat([img1,img2])
    # cv2.imshow("combined", im_h)
    if cv2.waitKey(5)  == 27:
        break
    elif cv2.waitKey(5) == ord("s"):
        cv2.imwrite("images/stereoLeft/imageL" + str(num)+ ".png", img1)
        cv2.imwrite("images/stereoRight/imageR"+str(num)+".png", img2)
        num+=1
        
    
    
cam1.release()
cam2.release()

cv2.destroyAllWindows()
    