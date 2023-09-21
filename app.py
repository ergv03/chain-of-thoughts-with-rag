import streamlit as st
from ui import render_url_container, render_apikey_container, render_question_container


st.set_page_config(page_title='Chain of Thoughts and Retrieval Augmented Generation')

with st.sidebar:
    render_apikey_container()

with st.container():
    render_url_container()

render_question_container()
