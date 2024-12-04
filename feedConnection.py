# Code to access a live CCTV Surveillance footage using OpenCV & Python.
## CCTV is currently present at my home and needs to be within the same LAN network for access.

import cv2 as cv

# Function to access laptop's camera.
def cameraAccess(feed=0):
    '''
    Default feed of a laptop's camera is 0. If you have external cameras, feel free to change to 1 or any other corresponding number.
    '''
    cap = cv.VideoCapture(feed)

    if not cap.isOpened():
        print("Camera Access Unavailable.")
        exit()
    else:
        while True:
            ret, frame = cap.read()

            if not ret:
                print("Frame Unavailable. Exit.")
                break
            
            # Shifting from BGR to Gray (optional)
            # frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            cv.imshow('VideoFeed',frame)

            if cv.waitKey(1) == ord('q'):
                break
        cap.release()
        cv.destroyAllWindows()

# cameraAccess()

# CCVT Surveillance Footage Access

