import streamlit as st
from ui import render_url_container, render_apikey_container, render_question_container
from openai_utils import load_openai_api_key
from llms import BrainstormProblemSolving
from search_indexing import download_and_index_documents

st.set_page_config(page_title='GVE - Retrieval Augmented Generation')

with st.sidebar:
    render_apikey_container()

with st.container():
    render_url_container()

render_question_container()

#
# with st.form('question-form', clear_on_submit=True):
#     query_text = st.text_area('Add your question here:', value=st.session_state.get('query_text', str()))
#     ask_button = st.form_submit_button('Ask')
#
# if ask_button:
#
#     load_openai_api_key()
#     st.session_state['query_text'] = query_text
#     cot = ChainOfThoughts(query_text, st.session_state.urls)
#
#     with st.status('Searching for an answer. Hold on tight, it may take up to 5 minutes...', expanded=True):
#         st.write('Downloading and indexing documents...')
#         cot.index = download_and_index_documents(st.session_state.urls)
#         st.write('Breaking down problem into smaller problems...')
#         cot.small_problems = cot.break_down_problem()
#         st.write('Starting brainstorming session...')
#         cot.solutions = cot.brainstorm_all_problems()
#         st.write('Brainstorming complete. Wrapping up a complete solution...')
#         response = cot.generate_big_solution()
#
#     # Display assistant response in chat message container
#     st.subheader('Response', divider='blue')
#     with st.container():
#         st.markdown(response)
#         for page_number, snippet in enumerate(cot.all_snippets):
#             display_relevant_snippets(page_number, snippet)
#
#     with st.expander('Debug'):
#         for problem, solution in zip(cot.small_problems, cot.solutions):
#             col1, col2 = st.columns(2)
#             with col1:
#                 st.markdown(problem)
#             with col2:
#                 st.markdown(solution)
