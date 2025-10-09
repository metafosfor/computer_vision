#I tried two trackers here - KCF and CSRT. Taking into account that
#cars are driving toward me (meaning toward camera), CSRT shows much better results.
#I think CSRT tracker could work better with scaled objects since the size of cars is 
#permanently increasing. KCF tracker usually gets lost after several frames. 

import cv2
from matplotlib import pyplot as plt
import sys
plt.rcParams['figure.figsize'] = [15, 10]

    
#tracker = cv2.TrackerKCF_create()  
tracker = cv2.TrackerCSRT_create()

cap = cv2.VideoCapture("videoplayback.mp4")

if not cap.isOpened():
    print("Error: OpenCV could not open the video stream using the URL.")
    sys.exit()
    
    
# Set the desired starting frame number
START_FRAME = 430
    
# Use CAP_PROP_POS_FRAMES to seek to the starting frame
print(f"Seeking to frame number {START_FRAME}...")
cap.set(cv2.CAP_PROP_POS_FRAMES, START_FRAME)
    
 # Read the frame 
ok, frame = cap.read()
if not ok:
    print('Cannot read video file')
    sys.exit()  
    
       
print("\nSelect the car to track using the mouse and press ENTER or SPACE.")
bbox = cv2.selectROI("Car Tracking Demo", frame, False, False)
cv2.destroyWindow("Car Tracking Demo")    
    
ok = tracker.init(frame, bbox)

i=0
while True:
    ok, frame = cap.read()

    if not ok:
        print("End of video stream.")
        break
        
    ok, bbox = tracker.update(frame)
    
    # Draw bounding box and status
    if ok:
        # Tracking success
        # Convert bounding box coordinates (float tuple) to integer values
        x, y = bbox[0], bbox[1]
        w, h = bbox[2], bbox[3]
                    
        # Draw the green rectangle around the tracked car
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2, 1)
            
        # Display tracker status
        cv2.putText(frame, " Tracker: Tracking", (20, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2)
    else:
        # Tracking failure
        cv2.putText(frame, " Tracker: Lost", (20, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)

    # Display FPS on frame
    cv2.putText(frame, "Frame Index: " + str(i), (20, 60), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 0, 0), 2)

    # Display result
    cv2.imshow("Car Tracking Demo", frame)

    # Exit if 'Q' is pressed
    k = cv2.waitKey(40) & 0xff
    if k == ord('q'):
        break
    
    i+=1

# 4. Clean up
cap.release()
cv2.destroyAllWindows()
    
    
