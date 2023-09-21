My attempt at combining Chain of Thoughts and Retrieval Augmented Generation.

Chain of Thoughts have proved to be a powerful technique in leveraging LLMs to solve complex problems and queries, by breaking down the problem into smaller steps that are solved one at a time.

Retrieval Augmented Generation helps alleviating hallucinations by providing to the LLM context, in the form of snippets from documents and websites that are relevant to the problem it's been asked to solve.

This app combines both techniques: given a list of documents provided by the user, and a problem to solve, the app will try to find a solution while taking into account the documents provided as reference. It does that by first breaking down the problem into smaller problems. Then, it will iterate through the smaller problems on at the time, and search for a solution using snippets extracted from the documents as part of the context.

Finally, it will combine all the found solutions into one "big" solution for the original problem.

A simple diagram with the workflow:

![image](https://github.com/ergv03/chain-of-thoughts-with-rag/assets/23053920/514bcb0e-1d33-4050-9cdc-f5bf09a9fc17)


Original Problem and Documents (in green) are provided by the user.

## Installation:

Just clone the repo and install the requirements using ```pip install -r requirements.txt```

**IMPORTANT:** Please be aware that several API calls will be done in the backend, so be mindful of the costs.

## How to run locally:

Run ```streamlit run app.py``` in your terminal.

Add your OpenAI API key in the sidebar, the URLs of the HTML/PDF documents that are relevant to your queries, and the problem to solve. Depending on the complexity of the problem/query, it may take up to 5 minutes for the algorithm to finish.

**Example:**

<img width="1732" alt="image" src="https://github.com/ergv03/chain-of-thoughts-with-rag/assets/23053920/61e95689-0f4a-4e1d-b64c-877561b5fc19">
