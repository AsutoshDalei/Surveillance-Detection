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

if "userNameState" not in st.session_state:
    st.session_state.userNameState = False
if "numFeedState" not in st.session_state:
    st.session_state.numFeedState = False

def userNameFnx():
    st.session_state.userNameState = True
def numFeedFnx():
    st.session_state.numFeedState = True

def sysConfigFnx():
    with st.form("sysConfigUser"):
        st.write("System Confurigation :computer:")
        userName = st.text_input(label="User Name",value=None,on_change=userNameFnx) 
        numFeeds = st.slider(label="Number of Camera Feeds",min_value=0,max_value=4,step=1,on_change=numFeedFnx)

        submitFlag = not((st.session_state.userNameState) and (st.session_state.numFeedState))
        submitted = st.form_submit_button("Submit Configuration",disabled=True)


with st.sidebar:
    st.title("SurveilAI Stats.")
    if st.button("Click To Configure System", type='primary'):
        sysConfigFnx()





