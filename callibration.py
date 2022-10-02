import cv2

cam1 = cv2.VideoCapture(0)
cam2 = cv2.VideoCapture(1)

num = 0

while cam1.isOpened():
    ret1, img1 = cam1.read()
    ret2, img2 = cam2.read()
    
    
    if ret1:
        cv2.imshow("img1", img1)
    if ret2:
        cv2.imshow("img2", img2)
        
        
    if cv2.waitKey(5)  == 27:
        break
    elif cv2.waitKey(5) == ord("s"):
        cv2.imwrite("images/stereoLeft/imageL" + str(num)+ ".png", img1)
        cv2.imwrite("images/stereoRight/imageR"+str(num)+".png", img2)
        num += 1
    
    
cam1.release()
cam2.release()
    
cv2.destroyAllWindows()
    