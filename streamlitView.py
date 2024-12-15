import cv2 as cv
import matplotlib.pyplot as plt
# import torch
import warnings
warnings.filterwarnings("ignore")
import streamlit as st

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
        st.session_state.userState['userName'] = st.text_input(label="User Name",value=None,help='Kindly provide your name.', disabled=st.session_state.disableConfig) 
        # st.session_state.userState['numFeeds'] = st.slider(label="Number of Camera Feeds (RTSP needed)",min_value=0,max_value=3,step=1,help='RTSP (Real-Time Streaming Protocol) is used for streaming media between devices, enabling real-time control over playback.')
        st.session_state.userState['numFeeds'] = st.segmented_control(label="Number of Camera Feeds (RTSP needed)",options=[0,1,2,3], default=0,help=RTSPDEFINATION, disabled=st.session_state.disableConfig)
   
    for feedPtr in range(st.session_state.userState['numFeeds']):
        st.session_state[f'feed{feedPtr+1}'] = {'name':'','link':None}
        with st.expander(f"Feed{feedPtr+1} Configuration"):
            st.session_state[f'feed{feedPtr+1}']['name'] = st.text_input("Feed Name:",f'Feed{feedPtr+1}',key=f'feed{feedPtr+1}Name')
            st.session_state[f'feed{feedPtr+1}']['link'] = st.text_input("RTSP Link:",None,key=f'feed{feedPtr+1}Link', disabled=st.session_state.disableConfig)

    st.divider()
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

if st.session_state.userState['userName'] != None:
    # st.caption(f"Hello {st.session_state.userState['userName']}")
    st.markdown(f"*Hello {st.session_state.userState['userName']}*")
st.divider()


if st.session_state.userState['numFeeds'] > 0:
    tabNames = []
    for feedPtr in range(st.session_state.userState['numFeeds']):
        tabNames.append(st.session_state[f'feed{feedPtr+1}']['name'])
    tabs = st.tabs(tabNames)

else:
    st.info('System Configuration Needed.', icon="ℹ️")








