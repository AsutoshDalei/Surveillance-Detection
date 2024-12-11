# Code to access a live CCTV Surveillance footage using OpenCV & Python.
## CCTV is currently present at my home and needs to be within the same LAN network for access.

import cv2 as cv
import matplotlib.pyplot as plt
import torch
import warnings
warnings.filterwarnings("ignore")

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

# RTSP (Real-Time Streaming Protocol) in CCTV Cameras:
# 
# RTSP is a network protocol used for controlling the delivery of streaming media, such as video from CCTV cameras.
# It is commonly used in surveillance systems to enable streaming of live footage from cameras to a client or a monitoring device.
# 
# The key features of RTSP:
# 
# 1. **Control Streaming Sessions**: RTSP allows clients to control the playback of streaming media. It can start, pause, stop, and seek video streams, making it ideal for real-time surveillance.
# 
# 2. **Two-way Communication**: RTSP supports bidirectional communication, meaning that it allows both the server (CCTV camera) and client (monitoring device or software) to exchange information. This is useful for features such as pan/tilt/zoom (PTZ) control on the camera.
# 
# 3. **Transport Independence**: RTSP is transport-independent, meaning it can work over various underlying protocols like TCP (Transmission Control Protocol) and UDP (User Datagram Protocol). This flexibility allows it to adapt to different network conditions and use cases.
# 
# 4. **Used in IP-based Surveillance**: RTSP is especially popular in modern IP-based CCTV systems, where cameras are connected to a network (e.g., local area network or internet). It allows video feeds from multiple cameras to be streamed to monitoring software or recording devices over a network.
# 
# 5. **RTSP URL Format**: An RTSP URL typically follows this format:
#    rtsp://<username>:<password>@<IP_address>:<port>/<stream_path>
#    Example: rtsp://admin:admin@192.168.1.100:554/stream1
#    This URL is used to access a live video feed from the CCTV camera.
# 
# 6. **Low Latency**: RTSP is designed for real-time streaming with low latency, making it suitable for security applications where timely delivery of video is essential.
# 
# 7. **Compression Support**: RTSP can be paired with video compression formats like H.264, MJPEG, or H.265 to optimize video quality and reduce bandwidth usage during transmission.
# 
# 8. **Limitations**: RTSP itself does not include mechanisms for video storage; it only controls the stream. To store recorded footage, RTSP streams are often integrated with network video recorders (NVRs) or other storage systems.
# 
# In summary, RTSP is a critical protocol for streaming live video feeds in modern CCTV surveillance systems, offering features like real-time control, low latency, and flexibility in transmission.


feedQuality = 0 #2K Resolution
feedQuality = 1 #Standard Resolution

outdoorCameraFeed = f'rtsp://HtiPNx9P:fy4YmtREZnzy2bJE@192.168.1.215:554/live/ch{feedQuality}'
indoorCameraFeed = f'rtsp://NELTJRSl:8z3Y969kgO6sGTpX@192.168.1.216:554/live/ch{feedQuality}'

def cameraAccessCCTV(feed):
    '''
    feed: RTSP Link to surveillance device. Need to be present in the same LAN network for access.
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
        
            gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            cv.imshow('frame', frame)
            if cv.waitKey(1) == ord('q'):
                break

        cap.release()
        cv.destroyAllWindows()

# cameraAccessCCTV(indoorCameraFeed)

# YoloV5n Model

cmap = [[255, 0, 0], [0, 255, 0], [0, 0, 255], [0, 255, 255], [255, 0, 255], [255, 255, 0], [255, 165, 0], [128, 0, 128], [0, 128, 255], [0, 255, 128]]
def plot_frame(frame,res,confidenceThreshold = 0.6):
    res = res[res.confidence >= confidenceThreshold]
    cmapPtr = 0
    for _,row in res.iterrows():
        color = cmap[cmapPtr]
        cmapPtr+=1
        xmin, ymin, xmax, ymax, cate, conf = row['xmin'],row['ymin'],row['xmax'],row['ymax'],row['name'],row['confidence']
        [xmin, ymin, xmax, ymax] = [int(i) for i in [xmin, ymin, xmax, ymax]]
        text = f'{cate}: {conf:0.2f}'
        frame = cv.rectangle(frame, (xmin,ymin), (xmax,ymax),thickness=2,color=color)
        frame = cv.putText(frame,text,(xmin,ymin-5),cv.FONT_HERSHEY_SIMPLEX,fontScale = 0.8,color=color,thickness = 2)
    return frame

model = torch.hub.load('ultralytics/yolov5', 'yolov5n', pretrained=True)

def cameraAccessCCTV_YOLO(feed,confidenceThreshold = 0.6):
    '''
    feed: RTSP Link to surveillance device. Need to be present in the same LAN network for access.
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

            predictions = model(frame).pandas().xyxy[0]
            framePred = plot_frame(frame.copy(),predictions,confidenceThreshold)
            
            cv.imshow('framePred', framePred)
            if cv.waitKey(1) == ord('q'):
                break

        cap.release()
        cv.destroyAllWindows()

        cameraAccessCCTV_YOLO(indoorCameraFeed,confidenceThreshold=0.1)

cameraAccessCCTV_YOLO(feed = indoorCameraFeed,confidenceThreshold = 0.1)