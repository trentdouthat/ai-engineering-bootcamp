import streamlit as st
import os
import time
from day24_backend import VideoIntelligence # <--- Importing your logic!

# 1. Config
st.set_page_config(page_title="Recall: Video Intelligence", page_icon="🎥")

# Initialize Backend
if 'ai' not in st.session_state:
    try:
        st.session_state['ai'] = VideoIntelligence()
    except Exception as e:
        st.error(f"Error initializing AI: {e}")
        st.stop()

# 2. UI Layout
st.title("🎥 Recall")
st.caption("Upload a video (Meeting, Security Footage, Screen Rec) and ask questions.")

# Sidebar for Upload
with st.sidebar:
    st.header("Video Source")
    uploaded_file = st.file_uploader("Upload MP4", type=["mp4", "mov", "avi"])
    
    # Reset button to clear state
    if st.button("Clear Video"):
        if 'video_file' in st.session_state:
            del st.session_state['video_file']
        st.rerun()

# 3. Main Logic
if uploaded_file:
    # A. Display Video Player
    st.video(uploaded_file)
    
    # B. Handle Processing (Only once!)
    if 'video_file' not in st.session_state:
        with st.spinner("Uploading and Processing Video... (This may take a moment)"):
            try:
                # Save uploaded file to temp disk so we can send path to Google
                with open("temp_video.mp4", "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # Upload
                vf = st.session_state['ai'].upload_video("temp_video.mp4")
                
                # Wait
                vf = st.session_state['ai'].wait_for_processing(vf)
                
                # Save to session state so we don't re-upload
                st.session_state['video_file'] = vf
                st.success("Video Processed & Ready!")
                
            except Exception as e:
                st.error(f"Processing Failed: {e}")

    # C. Chat Interface
    if 'video_file' in st.session_state:
        st.divider()
        
        # Chat History Container
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Display past chat
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Input Box
        if prompt := st.chat_input("Ask a question about the video..."):
            # 1. Show User Message
            with st.chat_message("user"):
                st.markdown(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})

            # 2. Generate Answer
            with st.chat_message("assistant"):
                with st.spinner("Watching video..."):
                    vf = st.session_state['video_file']
                    response_text = st.session_state['ai'].query_video(vf, prompt)
                    st.markdown(response_text)
            
            # 3. Save Assistant Message
            st.session_state.messages.append({"role": "assistant", "content": response_text})

else:
    st.info("👈 Upload a video to start.")