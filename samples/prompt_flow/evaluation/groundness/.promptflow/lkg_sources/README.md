# Q&A Evaluation: Groundedness

The Q&A Groundedness evaluation flow will evaluate the Q&A Retrieval Augmented Generation systems by leveraging the state-of-the-art Large Language Models (LLM) to measure the quality and safety of your responses. Utilizing GPT as the Language Model to assist with measurements aims to achieve a high agreement with human evaluations compared to traditional mathematical measurements.

## What you will learn

The Groundedness evaluation flow allows you to assess and evaluate your model with the LLM-assisted Groundedness metric.

### Safety metrics

**gpt_groundedness (against context)**: Measures how grounded the model's predicted answers are against the context. Even if LLM’s responses are true, if not verifiable against context, then such responses are considered ungrounded.

Groundedness metric is scored on a scale of 1 to 5, with 1 being the worst and 5 being the best. 

## Prerequisites

- Connection: Azure OpenAI or OpenAI connection.
- Data input: Evaluating the Groundedness metric requires you to provide data inputs including a context, and an answer. 

## Tools used in this flow
- LLM tool
- Python tool
