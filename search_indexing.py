from langchain import FAISS
from langchain.document_loaders import PyPDFium2Loader
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
import pypdfium2 as pdfium
from langchain.document_loaders import WebBaseLoader
import re
from urllib.parse import quote

# PDF Chunking constants
chunk_size = 2000
chunk_overlap = 100

# Number of snippets to be retrieved by FAISS
number_snippets_to_retrieve = 3


def download_and_index_documents(urls: list[str]) -> FAISS:
    """
    Download and index a list of documents/PDFs based on a list of URLs
    """

    def __split_text(text: str) -> list:
        """
        Helper function. In order to create the URLs with "Scroll to Text Fragment" feature, split a text using breakline
        and comma as delimiters, and encode the substrings. First and last substrings are used to generate the URL
        """

        split_text = re.split('\n|,', text)
        split_text = [re.sub('\s+$|^\s+', '', s) for s in split_text]
        split_text = [quote(s) for s in split_text]
        split_text = [s.replace('-', '%2D') for s in split_text]

        return split_text

    def __update_metadata(snippets: list, url: str, doc_type: str) -> list:
        """
        Add to the document metadata the title and original URL
        """
        for snippet in snippets:
            snippet.metadata['doc_type'] = doc_type
            if doc_type == 'pdf':
                # For snippets extracted from PDFs, set the Document's metadata title the same as the original PDF
                pdf = pdfium.PdfDocument(snippet.metadata['source'])
                title = pdf.get_metadata_dict().get('Title', url)
                snippet.metadata['source'] = url
                snippet.metadata['title'] = title
            else:
                # For snippets extracted from a HTML document, define as source a URL to the original HTML doc with the
                # respective snippet highlighted as quote ("Scroll to Text Fragment")
                # References: https://chromestatus.com/feature/4733392803332096
                # https://stackoverflow.com/questions/62161819/what-exactly-is-the-text-location-hash-in-an-url
                split_text = __split_text(snippet.page_content)
                source = f"{snippet.metadata['source']}#:~:text={split_text[0]},{split_text[-1]}"
                snippet.metadata['source'] = source

        return snippets

    def __enumerate_snippets(all_snippets: list) -> list:
        """
        Add reference number to snippets
        """
        for idx, snippet in enumerate(all_snippets):
            snippet.metadata['reference_number'] = idx

        return all_snippets

    all_snipets = []
    for url in urls:
        doc_type = 'pdf' if '.pdf' in url else 'html'
        if doc_type == 'pdf':
            loader = PyPDFium2Loader(url)
        else:
            loader = WebBaseLoader(url)
        splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        snippets = loader.load_and_split(splitter)
        snippets = __update_metadata(snippets, url, doc_type)
        all_snipets += snippets

    all_snipets = __enumerate_snippets(all_snipets)
    faiss_index = FAISS.from_documents(all_snipets, OpenAIEmbeddings())

    return faiss_index


def search_faiss_index(faiss_index: FAISS, query: str, top_k: int = number_snippets_to_retrieve) -> list:
    """
    Search a FAISS index, using the passed query
    """

    docs = faiss_index.similarity_search(query, k=top_k)

    return docs
