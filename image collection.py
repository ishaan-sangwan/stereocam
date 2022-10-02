import cv2

cap = cv2.VideoCapture(0)
cap2 = cv2.VideoCapture(1)

ret , img = cap.read()
ret2, img2 = cap2.read()
while True:
    ret, img = cap.read()
    ret2, img2 = cap2.read()
    
    if (ret):
        cv2.imshow("test", img)
    if (ret2):
        cv2.imshow("test 2", img2 )
    if cv2.waitKey(1) & 0xFF == ord("q") :
            break
        
cap.release()
cap2.release()
cv2.destroyAllWindows()