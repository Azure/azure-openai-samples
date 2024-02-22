# Q&A Evaluation: ada_similarity

The Q&A ada_similarity evaluation flow will evaluate the Q&A Retrieval Augmented Generation systems by leveraging LLM to measure the quality and safety of your responses. Utilizing GPT embedding model to assist with measurements aims to achieve a high agreement with human evaluations compared to traditional mathematical measurements.

## What you will learn

The Ada Similarity evaluation flow allows you to assess and evaluate your model with the LLM-assisted ada similarity metric. 


**ada_similarity**: Measures the cosine similarity of ada embeddings of the model prediction and the ground truth.

ada_similarity is a value in the range [0, 1]. 

## Prerequisites

- Connection: Azure OpenAI or OpenAI connection.
- Data input: Evaluating the Ada-Similarity metric requires you to provide data inputs including a question, a ground truth, and an answer. 

## Tools used in this flow
- Embedding tool
- Python Tool