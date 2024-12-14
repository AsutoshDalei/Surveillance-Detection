import cv2 as cv
import matplotlib.pyplot as plt
# import torch
import warnings
warnings.filterwarnings("ignore")

import streamlit as st


st.title("SurveilAI Platform")
st.markdown("Empowering Security with :red[Real-time Object Detection] and :blue[Intelligent Surveillance].")
st.divider()

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

if "agreement" not in st.session_state:
    agreement()

if "userState" not in st.session_state:
    st.session_state.userState = {'userName':None,'numFeeds':0,'config':False}


with st.sidebar:
    st.title("SurveilAI Stats Platform.")
    with st.expander("System Configuration"):
        st.session_state.userState['userName'] = st.text_input(label="User Name",value=None,help='Kindly provide your name.') 
        st.session_state.userState['numFeeds'] = st.slider(label="Number of Camera Feeds (RTSP needed)",min_value=0,max_value=3,step=1,help='RTSP (Real-Time Streaming Protocol) is used for streaming media between devices, enabling real-time control over playback.')

    for feedPtr in range(st.session_state.userState['numFeeds']):
        st.session_state[f'feed{feedPtr+1}'] = {'name':'','link':None}
        with st.expander(f"Feed{feedPtr+1} Configuration"):
            st.session_state[f'feed{feedPtr+1}']['name'] = st.text_input("Feed Name:",f'Feed{feedPtr+1}',key=f'feed{feedPtr+1}Name')
            st.session_state[f'feed{feedPtr+1}']['link'] = st.text_input("RTSP Link:",None,key=f'feed{feedPtr+1}Link')
    
    st.divider()
    # st.write(st.session_state.temp)

# st.write([st.session_state[f'feed{feedPtr+1}']['name']] for feedPtr in range(st.session_state.userState['numFeeds']))
st.write([st.session_state[f'feed{feedPtr+1}']['name']] for feedPtr in range(st.session_state.userState['numFeeds']))
# tabs = st.tabs([st.session_state[f'feed{feedPtr+1}']['name']] for feedPtr in range(st.session_state.userState['numFeeds']))








