import cv2 as cv
import matplotlib.pyplot as plt
import torch
import warnings
warnings.filterwarnings("ignore")
import streamlit as st

# FEED_out: rtsp://HtiPNx9P:fy4YmtREZnzy2bJE@192.168.1.215:554/live/ch0
# FEED_in: rtsp://NELTJRSl:8z3Y969kgO6sGTpX@192.168.1.216:554/live/ch0

# Image Processing Functions
cmap = [[255, 0, 0], [0, 255, 0], [0, 0, 255], [0, 255, 255], [255, 0, 255], [255, 255, 0], [255, 165, 0], [128, 0, 128], [0, 128, 255], [0, 255, 128]]
def plot_frame(frame,res,confidenceThreshold = 0.6):
    res = res[res.confidence >= confidenceThreshold]
    cmapPtr = 0
    for _,row in res.iterrows():
        color = cmap[cmapPtr]
        cmapPtr+=1
        xmin, ymin, xmax, ymax, cate, conf = row['xmin'],row['ymin'],row['xmax'],row['ymax'],row['name'],row['confidence']
        [xmin, ymin, xmax, ymax] = [int(i) for i in [xmin, ymin, xmax, ymax]]
        # c = [255,0,0]
        text = f'{cate}: {conf:0.2f}'
        frame = cv.rectangle(frame, (xmin,ymin), (xmax,ymax),thickness=2,color=color)
        frame = cv.putText(frame,text,(xmin,ymin-5),cv.FONT_HERSHEY_SIMPLEX,fontScale = 0.8,color=color,thickness = 2)
    return frame


# Prediction Engine
@st.cache_resource
def fetchEngine(modelSetup = 'YOLOv5 nano'):
    modelMap = {
        'YOLOv5 nano':torch.hub.load('ultralytics/yolov5', 'yolov5n', pretrained=True),
        'YOLOv5 small':torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
                }
    model = modelMap[modelSetup]
    return model


def predictionEngine(frame,confidenceThreshold = 0.6):
    predictions = model(frame).pandas().xyxy[0]
    framePred = plot_frame(frame.copy(),predictions,confidenceThreshold)
    return framePred


# Vision Functions
def cameraAccessMultiFeed(feeds,feednames,stElems,elemNums):
    '''
    feed: RTSP Link to surveillance device. Need to be present in the same LAN network for access.
    '''
    feedMap,stMap,stButton,frameHolder = {},{},{},{}
    for feed,stElem,elemNum in zip(feeds,stElems,range(elemNums)):
        feedMap[f'feed{elemNum}'] = cv.VideoCapture(feed)
        if not feedMap[f'feed{elemNum}'].isOpened():
            stMap[f'feed{elemNum}'].error("Camera Access Unavailable", icon="🚨")
        else:
            stButton[f'feed{elemNum}'] = stElem.button("Stop Feed",help='Click to stop the feed.',key=f'feed{elemNum}Bt')
            frameHolder[f'feed{elemNum}'] = stElem.empty()
  
    while resetButton != True:
        for elemNum in range(elemNums):
            if (feedMap[f'feed{elemNum}'].isOpened()) and (not stButton[f'feed{elemNum}']):
                ret, frame = feedMap[f'feed{elemNum}'].read()
                if not ret:
                    stElem[f'feed{elemNum}'].error("Frame Unavailable.", icon="🚨")
                    break
                gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
                frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
                # frameHolder[f'feed{elemNum}'].image(frame)

                # After Prediction.
                framePred = predictionEngine(frame)
                frameHolder[f'feed{elemNum}'].image(framePred)


    for elemNum in range(elemNums):
        feedMap[f'feed{elemNum}'].release()



# Extras
RTSPDEFINATION = 'RTSP (Real-Time Streaming Protocol) is used for streaming media between devices, enabling real-time control over playback.'

@st.dialog("Warning: Responsible Use of SurveilAI")
def agreement():
    agreementContent = ''' :warning:
By using this platform, you acknowledge:

* :orange[Privacy Compliance:] Ensure your use of surveillance data complies with all privacy laws and regulations.
* :orange[Intended Use:] This platform is for security purposes only. Unauthorized or unethical use is prohibited.
* :orange[Detection Accuracy:] AI detection may vary in accuracy—always verify critical detections.
* :orange[Data Security:] Protect your account and ensure secure handling of video feeds and alerts.
'''
    st.markdown(agreementContent)
    userName = st.text_input("Name", help='Your name.')
    userEmail = st.text_input("Email ID", help='Your e-mail ID')
    if st.checkbox("Proceed only if you understand and agree to these terms."):
        st.session_state.agreement = {'status':True,'name':userName,'email':userEmail}
    else:
        st.session_state.agreement = {'status':False,'name':userName,'email':userEmail}

# Session States
if "agreement" not in st.session_state:
    agreement()

if "userState" not in st.session_state:
    st.session_state.userState = {'userName':None,'numFeeds':0,'modelSetup':'yolov5n'}

if "disableConfig" not in st.session_state:
    st.session_state.disableConfig = False

def disableFnx(status):
    st.session_state.disableConfig = status


# Sidebar Section
with st.sidebar:
    st.title("SurveilAI Stats Platform.")
    with st.expander("System Configuration"):
        st.session_state.userState['userName'] = st.text_input(label="User Name",value=None,help='Kindly provide your name.', disabled=st.session_state.disableConfig, placeholder='', max_chars= 50) 
        st.session_state.userState['numFeeds'] = st.segmented_control(label="Number of Camera Feeds (RTSP needed)",options=[0,1,2,3], default=0,help=RTSPDEFINATION, disabled=st.session_state.disableConfig)
        st.session_state.userState['modelSetup'] = st.selectbox(label='Select Model', options=['YOLOv5 nano','YOLOv5 small'],disabled=st.session_state.disableConfig)
   
    for feedPtr in range(st.session_state.userState['numFeeds']):
        st.session_state[f'feed{feedPtr+1}'] = {'name':'','link':None}
        with st.expander(f"Feed{feedPtr+1} Configuration"):
            st.session_state[f'feed{feedPtr+1}']['name'] = st.text_input("Feed Name:",f'Feed{feedPtr+1}',key=f'feed{feedPtr+1}Name')
            st.session_state[f'feed{feedPtr+1}']['link'] = st.text_input("RTSP Link:",None,key=f'feed{feedPtr+1}Link', disabled=st.session_state.disableConfig)

    st.divider()
    with st.expander("System Health"):
        st.write("Work pending")
    st.divider()
    sideBarcol1, sideBarcol2 = st.columns(2)
    with sideBarcol1:
        submitButton = st.button("Submit Setup", help="Click to submit configurations.")
        if submitButton:
            with st.spinner("Setting Up"):
                disableFnx(True)
                model = fetchEngine(modelSetup=st.session_state.userState['modelSetup'])
            st.success('Setup', icon="✅")
            
    with sideBarcol2:
        resetButton = st.button("Reset Setup", type = 'primary', help='Click to reset configurations.')
        if resetButton:
            disableFnx(False)
            st.rerun()

# Primary Section
st.title("SurveilAI Platform")
st.markdown("Empowering Security with :red[Real-time Object Detection] and :blue[Intelligent Surveillance].")

st.divider()

if (submitButton == True) and (st.session_state.userState['numFeeds'] > 0):
    tabNames = [st.session_state[f'feed{feedPtr+1}']['name'] for feedPtr in range(st.session_state.userState['numFeeds'])]
    feedLinks = [st.session_state[f'feed{feedPtr+1}']['link'] for feedPtr in range(st.session_state.userState['numFeeds'])]
    tabs = st.tabs(tabNames)

    cameraAccessMultiFeed(feeds=feedLinks,feednames=tabNames,stElems=tabs,elemNums=st.session_state.userState['numFeeds'])

else:
    st.info('System Configuration Needed.', icon="ℹ️")








