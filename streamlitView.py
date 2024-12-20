import cv2 as cv
import matplotlib.pyplot as plt
# import torch
import warnings
warnings.filterwarnings("ignore")
import streamlit as st

# FEED: rtsp://NELTJRSl:8z3Y969kgO6sGTpX@192.168.1.216:554/live/ch0

# Vision Functions
def cameraAccessCCTV(feed,feedname, stElement):
    '''
    feed: RTSP Link to surveillance device. Need to be present in the same LAN network for access.
    '''
    stopbutton = stElement.button("Stop Feed",help='Click to stop the feed.')
    framePlaceholder = stElement.empty()
    # framePlaceholder.image()


    cap = cv.VideoCapture(feed)
    if not cap.isOpened():
        # print("Camera Access Unavailable.")
        stElement.error("Camera Access Unavailable.", icon="🚨")
        exit()
    else:  
        while cap.isOpened() and not stopbutton:
            ret, frame = cap.read()
            if not ret:
                # print("Frame Unavailable. Exit.")
                stElement.error("Frame Unavailable.", icon="🚨")
                break
            gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            framePlaceholder.image(frame)
        
        cap.release()

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
    st.session_state.userState = {'userName':None,'numFeeds':0,'config':False}

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
        if st.button("Submit Setup", help="Click to submit configurations."):
            disableFnx(True)
            st.success('Setup', icon="✅")
            

    with sideBarcol2:
        if st.button("Reset Setup", type = 'primary', help='Click to reset configurations.'):
            disableFnx(False)
            st.rerun()

# Primary Section
st.title("SurveilAI Platform")
st.markdown("Empowering Security with :red[Real-time Object Detection] and :blue[Intelligent Surveillance].")

# Seems Unnecessary
# if st.session_state.userState['userName'] != None:
#     st.markdown(f"*For {st.session_state.userState['userName']}.*")
st.divider()

if st.session_state.userState['numFeeds'] > 0:
    tabNames = []
    for feedPtr in range(st.session_state.userState['numFeeds']):
        tabNames.append(st.session_state[f'feed{feedPtr+1}']['name'])
    tabs = st.tabs(tabNames)

    for feedTab,nameTab,feedPtr in zip(tabs,tabNames,range(st.session_state.userState['numFeeds'])):
        feedTab.subheader(nameTab)
        feedLink = st.session_state[f'feed{feedPtr+1}']['link']

        cameraAccessCCTV(feed=feedLink, feedname=nameTab, stElement=feedTab)





else:
    st.info('System Configuration Needed.', icon="ℹ️")








