import streamlit as st
import pandas as pd
import google.generativeai as genai
import time
import requests
import os
from streamlit_lottie import st_lottie

# 1. BRAIN SETUP
API_KEY = "AIzaSyD-0zM_rIjHQMKtw_Ywl0v0DioQEXCA9Yc"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-3-flash-preview')

# 2. THE BLUEPRINT (Theme & Click-Fix)
st.set_page_config(page_title="The Nexus AI", page_icon="🌐", layout="centered")

st.markdown("""
    <style>
    /* Deep Navy Background */
    .stApp { 
        background-color: #001f3f; 
        color: #FFFFFF; 
    }
    
    /* Blue Chat Bubbles */
    [data-testid="stChatMessage"] { 
        background-color: #003366; 
        border-radius: 15px; 
        border: 1px solid #00509d;
    }
    
    /* Blue Airplane 'Send' Icon */
    [data-testid="stChatInputButton"] { color: #85C1E9 !important; }
    
    /* Fix: Ensures the input box is clickable and on top */
    .stChatInputContainer {
        z-index: 9999 !important;
    }

    /* Spinner Color */
    .stSpinner > div { border-top-color: #85C1E9 !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. BLUE SPLASH SCREEN (Safety Catch Included)
def load_lottieurl(url):
    try:
        r = requests.get(url, timeout=5)
        return r.json() if r.status_code == 200 else None
    except: return None

lottie_blue = load_lottieurl("https://lottie.host/8816f0e4-f3a3-4852-875c-352b21696614/TfTfTfTf.json")

if 'ready' not in st.session_state:
    placeholder = st.empty()
    with placeholder.container():
        if lottie_blue:
            st_lottie(lottie_blue, height=300)
        st.markdown("<h2 style='text-align: center; color: #85C1E9;'>SYNCHRONIZING NEXUS...</h2>", unsafe_allow_html=True)
        time.sleep(2.5)
    st.session_state.ready = True
    placeholder.empty()

# 4. LOGO & HEADER
if os.path.exists("logo.png"):
    st.logo("logo.png", size="large")

st.title("The Nexus")
st.write("Find your squad.")

# 5. DATA LOADING
try:
    df = pd.read_csv('STEP1.csv')
    knowledge = df.to_string(index=False)
except:
    st.error("Error: Could not find STEP1.csv")
    knowledge = ""

# 6. THE CHAT INTERFACE
if user_query := st.chat_input("Tell the Nexus your interests..."):
    # Display user query
    with st.chat_message("user", avatar="👤"):
        st.write(user_query)
    
    # Display AI response
    with st.chat_message("assistant", avatar="🚀"):
        if knowledge:
            with st.spinner("Decoding..."):
                prompt = f"Data: {knowledge}\nStudent: {user_query}\nRecommend 2 clubs."
                response = model.generate_content(prompt)
                st.write(response.text)
        else:
            st.error("I don't have the club list data to help you yet!")