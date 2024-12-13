import cv2 as cv
import matplotlib.pyplot as plt
import torch
import warnings
warnings.filterwarnings("ignore")

import streamlit as st


st.title("SurveilAI Platform")
# st.subheader("Empowering Security with Real-time Object Detection and Intelligent Surveillance")
st.markdown("Empowering Security with :red[Real-time Object Detection] and :blue[Intelligent Surveillance].")
st.divider()

global disableAgreement
global signed

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
    st.session_state.signed = st.checkbox("Proceed only if you understand and agree to these terms.", value=False)

if ("agreement" not in st.session_state) or (st.session_state.signed==False):
    agreement()
print(("agreement" not in st.session_state), st.session_state.signed)


