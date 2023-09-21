import re
import streamlit as st
from openai_utils import load_openai_api_key
from llms import BrainstormProblemSolving
from search_indexing import download_and_index_documents


def remove_url(url_to_remove):
    """
    Remove URLs from the session_state. Triggered by the respective button
    """
    if url_to_remove in st.session_state.urls:
        st.session_state.urls.remove(url_to_remove)


def format_url(url: str) -> str:
    """
    Format URL to include only the domain and document path. For example:
    https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9300/hardware/install/b_c9300_hig/b_c9300_hig_chapter_010.pdf
    becomes:
    https://www.cisco.com/.../b_c9300_hig_chapter_010.pdf
    """

    formatted_url = re.split('https?:\/\/', url)[-1]
    formatted_url = formatted_url.split('/')
    formatted_url = f"{formatted_url[0]}/.../{formatted_url[-1]}"

    return formatted_url


def display_relevant_snippets(snippet_number, snippet):
    """
    Display relevant snippets for each chat message
    """
    snippet_header = f'Relevant snippet ({snippet_number})'
    with st.expander(snippet_header):
        st.markdown(f"[Link to snippet:]({snippet.metadata['source']})")
        st.markdown(snippet.page_content)


def render_apikey_container():
    """
    Render API key container
    """

    st.subheader('API Key', divider='blue')
    with st.expander('Add your API key here', expanded=True):
        st.text_input('OpenAI API Key:', type='password', key='openai_api_key')


def render_url_container():
    """
    Render Add/Remove URLs form/container
    """

    if 'urls' not in st.session_state:
        st.session_state.urls = []

    # Add/Remove URLs form
    st.subheader('Add Websites and PDFs here', divider='blue', anchor=False)
    with st.form('urls-form', clear_on_submit=True):
        url = st.text_input('URLs to relevant websites and PDFs. Multiple documents can be added:', autocomplete='url')
        add_url_button = st.form_submit_button('Add')
        if add_url_button:
            if url not in st.session_state.urls:
                st.session_state.urls.append(url)

    # Display a container with the URLs added by the user so far
    with st.container():
        if st.session_state.urls:
            st.subheader('URLs added', anchor=False)
            for url in st.session_state.urls:
                url_col1, url_col2 = st.columns([0.7, 0.3])
                formatted_url = format_url(url)
                with url_col1:
                    st.markdown(f"[{formatted_url}]({url})")
                with url_col2:
                    st.button(label='Remove', key=f"Remove {url}", on_click=remove_url, kwargs={'url_to_remove': url})
                st.divider()


def render_question_container():
    """
    Render question container/form.
    """

    st.subheader('Problem to solve', divider='blue', anchor=False)
    with st.form('question-form', clear_on_submit=False):
        query_text = st.text_area('Add your problem here:')
        ask_button = st.form_submit_button('Ask')

    if ask_button:

        # Reload API key just in case
        load_openai_api_key()
        st.session_state['query_text'] = query_text
        brainstorm = BrainstormProblemSolving(query_text)

        with st.status('Searching for an answer. Hold on tight, it may take up to 5 minutes...', expanded=True):
            st.write('Downloading and indexing documents...')
            brainstorm.index = download_and_index_documents(st.session_state.urls)
            st.write('Breaking down problem into smaller problems...')
            brainstorm.small_problems = brainstorm.break_down_problem()
            st.write('Starting brainstorming session...')
            brainstorm.solutions = brainstorm.brainstorm_all_problems()
            st.write('Brainstorming complete. Wrapping up a complete solution...')
            response = brainstorm.summarize_solution()

        # Display assistant response in chat message container
        st.subheader('Response', divider='blue')
        with st.container():
            st.markdown(response)
            for idx, snippet in enumerate(brainstorm.all_snippets):
                display_relevant_snippets(idx, snippet)

        with st.expander('Debug'):
            for problem, solution in zip(brainstorm.small_problems, brainstorm.solutions):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(problem)
                with col2:
                    st.markdown(solution)
