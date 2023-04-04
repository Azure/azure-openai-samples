# Document Analysis using OpenAI GPT-3
This repository provides a set of examples for performing document analysis using OpenAI's GPT-3 language model. They are: 

1. **Data Exploration** - Explore data used in this repo. 
2. **Get Embeddings** - Generate embeddings from documents using GPT-3.
3. **Visualise Embeddings** - Visualise embeddings in 3D plot. 
4. **Classify Documents** - Use GPT-3 to classify documents into different categories.
5. **Summarize Documents** - Automatically generate summaries of documents using GPT-3.
6. **Extract Key Information** - Identify key information in documents using GPT-3.
7. **Extract Key Words** - Extract important words from documents using GPT-3.
8. **Semantic Search** - Retrieve relevant documents. 
9. **Retrieve Information based on Context** - Answer a query based on given context. 
10. **Unstructured Data to Structured Data** - Extract specified entities and put into a table. 

# BBC News Articles Analysis
This project is a data analysis of the BBC news dataset. The goal of this project is to explore the data, classify documents into categories, summarize documents, extract key information from documents and extract keywords from documents. 

## Dataset
The dataset used in this project is the [BBC News Archive](https://www.kaggle.com/datasets/hgultekin/bbcnewsarchive) available from [kaggle](www.kaggle.com). It contains 2225 articles from the BBC news website with 5 different categories: business, entertainment, politics, sport and tech. Each article has a category, filename, title and text.

## Language Model
Examples in this repo uses `text-davinci-003`. 
## Notebooks
This project consists of notebooks that perform the following tasks:

1. [00-explore-data.ipynb](./notebooks/00-explore-data.ipynb) - This notebook explores the data by looking at the distribution of classes, number of words per document, etc.
2. [01-get-embeddings.ipynb](./notebooks/01-get-embeddings.ipynb) - This notebook uses pre-trained word embeddings to create vector representations for each document.
3. [02-visualise-embeddings.ipynb](./notebooks/02-visualise-embeddings.ipynb) - This notebooks visualise word embeedings in a 3D plot. 
4. [03-classify-documents.ipynb](./notebooks/03-classify-documents.ipynb) - This notebook builds classification models using Random Forest and XGBoost to predict the class of each document.
5. [04-summarize-documents.ipynb](./notebooks/04-summarize-documents.ipynb) - This notebook uses GPT-3 to generate summaries for each document.
6. [05-extract-key-information.ipynb](./notebooks/05-extract-key-information.ipynb) - This notebook extracts key information from each document such as people, organizations, locations, etc.
7. [06-extract-key-words.ipynb](./notebooks/06-extract-key-words.ipynb) - This notebook extracts important keywords from each document.
8. [07-semantic-search.ipynb](./notebooks/07-semantic-search.ipynb) - This notebook performs semantic search to retreive most relevant news from a specific corpus, by comparing the similiarity of the embeddings of the query to that of the text corpus.
9. [08-retrieve-information.ipynb](./notebooks/08-retrieve-information.ipynb) This notebook retrieve information based on a given context. This is achieved by contstructing the prompt with context. 
10. [09-unstructure-data-to-structured-data.ipynb](./notebooks/09-unstructure-data-to-structured-data.ipynb) This notebook extract specified entities and arranged them into a table. 

*Note: This README.md is co-authored with `text-davinci-003`.*

## References
- OpenAI repo: https://github.com/openai/openai-cookbook/ 
- Which embedding model to use? https://openai.com/blog/new-and-improved-embedding-model/ 

