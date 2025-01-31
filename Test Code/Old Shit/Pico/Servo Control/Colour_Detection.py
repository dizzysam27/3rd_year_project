import cv2
import  numpy as np
from PIL import Image

def get_limits(colour):
    
    c = np.uint8([[colour]])
    hsvC = cv2.cvtColor(c, cv2.COLOR_BGR2HSV)

    lowerLimit = hsvC[0][0][0] - 1,100,100
    upperLimit = hsvC[0][0][0] + 1,255,255

    lowerLimit = np.array(lowerLimit, dtype=np.uint8)
    upperLimit = np.array(upperLimit, dtype=np.uint8)

    return lowerLimit, upperLimit

cap = cv2.VideoCapture(0)
yellow = [0, 255, 255]

while True:
    ret, frame = cap.read()
    hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

# Colour 1
    lowerLimit, upperLimit = get_limits(colour=yellow)
    mask = cv2.inRange(hsvImage, lowerLimit, upperLimit)
    
    mask_ = Image.fromarray(mask)
    bbox1 = mask_.getbbox()

    print(bbox1)

    if bbox1 is not None:
        x1,y1,x2,y2 = bbox1
        frame = cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,255),5)

# # Colour 2  
#     lowerLimit, upperLimit = get_limits(colour=red)
#     mask = cv2.inRange(hsvImage, lowerLimit, upperLimit)
    
#     mask_ = Image.fromarray(mask)
#     bbox2 = mask_.getbbox()

#     print(bbox2)

#     if bbox2 is not None:
#         x1,y1,x2,y2 = bbox2
#         frame = cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),5)

    cv2.imshow('frame',frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()