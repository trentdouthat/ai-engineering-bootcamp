import streamlit as st
import pandas as pd
from day24_backend import VideoIntelligence

# 1. Config
st.set_page_config(page_title="Recall Pro", page_icon="🎥", layout="wide")

if 'ai' not in st.session_state:
    st.session_state['ai'] = VideoIntelligence()

# 2. Sidebar (Upload)
with st.sidebar:
    st.header("🎥 Video Source")
    uploaded_file = st.file_uploader("Upload MP4", type=["mp4", "mov", "avi"])
    
    if st.button("Reset App"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# 3. Main Layout
st.title("Recall Pro: Video Intelligence")

if uploaded_file:
    # A. Display Video
    st.video(uploaded_file)
    
    # B. Processing & Timeline Generation
    if 'video_file' not in st.session_state:
        with st.spinner("Processing Video & Generating Timeline..."):
            try:
                # 1. Upload & Wait
                with open("temp_video.mp4", "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                vf = st.session_state['ai'].upload_video("temp_video.mp4")
                vf = st.session_state['ai'].wait_for_processing(vf)
                st.session_state['video_file'] = vf
                
                # 2. Generate Timeline (The New Feature)
                timeline_data = st.session_state['ai'].get_video_timeline(vf)
                st.session_state['timeline'] = timeline_data
                
                st.success("Analysis Complete!")
                
            except Exception as e:
                st.error(f"Error: {e}")

    # C. Display Timeline
    if 'timeline' in st.session_state:
        with st.expander("📅 Video Timeline (Generated Automatically)", expanded=True):
            df = pd.DataFrame(st.session_state['timeline'])
            st.dataframe(
                df,
                use_container_width=True,
                column_config={
                    "start": st.column_config.TextColumn("Start", width="small"),
                    "end": st.column_config.TextColumn("End", width="small"),
                    "event_description": st.column_config.TextColumn(
                        "Event Description", 
                        width="large" # Allocates remaining space to this column
                    ),
                }
            )
    # D. Q&A Interface
    if 'video_file' in st.session_state:
        st.divider()
        st.subheader("💬 Chat with Video")

        # Chat History
        if "messages" not in st.session_state:
            st.session_state.messages = []

        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        if prompt := st.chat_input("Ask about specific details..."):
            with st.chat_message("user"):
                st.markdown(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})

            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    vf = st.session_state['video_file']
                    ans = st.session_state['ai'].query_video(vf, prompt)
                    st.markdown(ans)
            st.session_state.messages.append({"role": "assistant", "content": ans})

else:
    st.info("Upload a video to see the magic.")