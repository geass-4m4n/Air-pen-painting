import numpy as np
import cv2
from collections import deque

# Define the upper and lower boundaries for a color to be considered "red"
blueLower = np.array([161, 155, 84])
blueUpper = np.array([179, 255, 255])

#blueLower = np.array([100, 60, 60])
#blueUpper = np.array([140, 255, 255])

#green
blueLower = np.array([45, 100, 50])
blueUpper = np.array([75, 255, 255])

# Define a 5x5 kernel for erosion and dilation
kernel = np.ones((5, 5), np.uint8)

# Initialize deques to store different colors in different arrays
bpoints = [deque(maxlen=512)]
gpoints = [deque(maxlen=512)]
rpoints = [deque(maxlen=512)]
ypoints = [deque(maxlen=512)]

# Initialize an index variable for each of the colors 
bindex = 0
gindex = 0
rindex = 0
yindex = 0

# Blue, Green, Red, Yellow respectively
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)] 
colorIndex = 1

paintWindow = np.zeros((471,636,3)) + 255
# Draw buttons like colored rectangles on the white image
paintWindow = cv2.rectangle(paintWindow, (40,1), (140,100), (0,0,0), 2)
paintWindow = cv2.rectangle(paintWindow, (160,1), (255,100), colors[0], -1)
paintWindow = cv2.rectangle(paintWindow, (275,1), (370,100), colors[1], -1)
paintWindow = cv2.rectangle(paintWindow, (390,1), (485,100), colors[2], -1)
paintWindow = cv2.rectangle(paintWindow, (505,1), (600,100), colors[3], -1)

# Label the rectanglular boxes drawn on the image
cv2.putText(paintWindow, "CLEAR ALL", (49, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
#cv2.putText(paintWindow, "BLUE", (185, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
#cv2.putText(paintWindow, "GREEN", (298, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
#cv2.putText(paintWindow, "RED", (420, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
#cv2.putText(paintWindow, "YELLOW", (520, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150,150,150), 2, cv2.LINE_AA)



camera = cv2.VideoCapture(0)


while(True):
    
    (grabbed, frame) = camera.read()
    frame = cv2.flip(frame, 1) #mirror image karo bhai
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    if not grabbed:
        break   
    # Add the same paint interface to the camera feed captured through the webcam (for ease of usage)
    frame = cv2.rectangle(frame, (40,25), (140,100), (122,122,122), -1)
    frame = cv2.rectangle(frame, (160,25), (255,100), colors[0], -1)
    frame = cv2.rectangle(frame, (275,25), (370,100), colors[1], -1)
    frame = cv2.rectangle(frame, (390,25), (485,100), colors[2], -1)
    frame = cv2.rectangle(frame, (505,25), (600,100), colors[3], -1)
    cv2.putText(frame, "CLEAR ALL", (49, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "BLUE", (185, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "GREEN", (298, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "RED", (420, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "YELLOW", (520, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150,150,150), 2, cv2.LINE_AA)
    
    blueMask = cv2.inRange(hsv, blueLower, blueUpper)
    blueMask = cv2.erode(blueMask, kernel, iterations=2)
    blueMask = cv2.morphologyEx(blueMask, cv2.MORPH_OPEN, kernel)
    blueMask = cv2.dilate(blueMask, kernel, iterations=1)
      # Find contours in the image
    (cnts, h) = cv2.findContours(blueMask.copy(), cv2.RETR_EXTERNAL,
    	cv2.CHAIN_APPROX_SIMPLE)
    
    
    
    if len(cnts) > 0:
    	# Sort the contours and find the largest one -- we assume this contour correspondes to the area of the bottle cap
        cnt = sorted(cnts, key = cv2.contourArea, reverse = True)[0]
        # Get the radius of the enclosing circle around the found contour
        ((x, y), radius) = cv2.minEnclosingCircle(cnt)
       # Draw the circle around the contour
        cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
        # Get the moments to calculate the center of the contour
        M = cv2.moments(cnt)
        center = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))
        
        
        
        if center[1] <= 100:
            if 40 <= center[0] <= 140: # Clear All
                bpoints = [deque(maxlen=512)]
                gpoints = [deque(maxlen=512)]
                rpoints = [deque(maxlen=512)]
                ypoints = [deque(maxlen=512)]

                bindex = 0
                gindex = 0
                rindex = 0
                yindex = 0
                
                paintWindow[67:,:,:] = 255
                
                
                
            elif 160 <= center[0] <= 255:
                    colorIndex = 0 # Blue
                    
            elif 275 <= center[0] <= 370:
                    colorIndex = 1 # Green
                    
            elif 390 <= center[0] <= 485:
                    colorIndex = 2 # Red
                    
            elif 505 <= center[0] <= 600:
                    colorIndex = 3 # Yellow
        else :
            
            if colorIndex == 0:
                bpoints[bindex].appendleft(center)
                
            elif colorIndex == 1:
                gpoints[gindex].appendleft(center)
                
                
            elif colorIndex == 2:
                rpoints[rindex].appendleft(center)
                
            elif colorIndex == 3:
                ypoints[yindex].appendleft(center)        
    
    
    
    # Append the next deque when no contours are detected 
    else:
        bpoints.append(deque(maxlen=512))
        bindex += 1
        gpoints.append(deque(maxlen=512))
        gindex += 1
        rpoints.append(deque(maxlen=512))
        rindex += 1
        ypoints.append(deque(maxlen=512))
        yindex += 1        
     

           
    
    # Draw lines of all the colors (Blue, Green, Red and Yellow)
    points = [bpoints, gpoints, rpoints, ypoints] 
    
    
    
    
    
    for i in range(len(points)):
        for j in range(len(points[i])):
            for k in range(1, len(points[i][j])):
                if points[i][j][k - 1] is None or points[i][j][k] is None:
                    continue
                cv2.line(frame, points[i][j][k - 1], points[i][j][k], colors[i], 2)
                cv2.line(paintWindow, points[i][j][k - 1], points[i][j][k], colors[i], 2)

    
    
    cv2.drawContours(frame, cnts, -1, (0,255,0), 3)

    cv2.imshow('frame',frame)   
    cv2.imshow('paint',paintWindow)
    cv2.imshow('paintp',blueMask)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
camera.release()
cv2.destroyAllWindows()