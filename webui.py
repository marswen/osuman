import os
import config
import shutil
import tempfile
import pandas as pd
import streamlit as st
from run_analysis import RunAnalysis
from langchain_community.chat_models import ChatOpenAI, ChatTongyi
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler


def demo_page():
    st.header('🤖 OSUMAN')
    st.subheader('Clinical data analytics agent')
    uploaded_file = st.file_uploader(
        "Please upload CSV format data",
        type=['csv',],
        label_visibility="collapsed",
    )
    if st.button('Start'):
        with st.spinner(f"Thinking"):
            with tempfile.NamedTemporaryFile() as tf:
                tf.write(uploaded_file.getbuffer())
                shutil.copy(tf.name, os.path.join(os.path.dirname(__file__), 'data.csv'))
            if config.model_name.startswith('gpt'):
                chat_llm = ChatOpenAI(model_name=config.model_name, temperature=0.1, streaming=True)
            if config.model_name.startswith('qwen'):
                chat_llm = ChatTongyi(model=config.model_name, temperature=0.1, streaming=True)
            std_callback = StreamingStdOutCallbackHandler()
            callbacks = [std_callback]
            data = pd.read_csv('./data.csv')
            st.session_state["analyzer"] = RunAnalysis(chat_llm, callbacks, data)
            st.session_state["analyzer"].generate_topic()
    if 'analyzer' in st.session_state:
        topic_generate_display = '\n\n'.join([f"{i}. **{topic['title']}**\n{topic['description']}" for i, topic in enumerate(st.session_state["analyzer"].topic_generate_json)])
        st.markdown('I have come up with the following five topics for you. Please choose one topic for analysis:')
        st.markdown(topic_generate_display)
        st.session_state["topic_select_id"] = st.radio(
            "Select Topic Number",
            key="visibility",
            options=list(range(5)),
            horizontal=True
        )
        if st.button('Continue'):
            with st.spinner(f"Thinking"):
                logs = st.session_state["analyzer"].generate_code(int(st.session_state["topic_select_id"]))
                for log in logs:
                    st.code(log, language='r')


if __name__ == '__main__':
    demo_page()
