# Chat with Wikipedia

This is a companion sample flow to "Ask Wikipedia". It demonstrates how to create a chatbot that can remember previous interactions and use the conversation history to generate next message.

## What you will learn

In this flow, you will learn
- how to compose a chat flow.
- prompt template format of LLM tool chat API. Message delimiter is a separate line containing role name and colon: "system:", "user:", "assistant:".
See <a href="https://platform.openai.com/docs/api-reference/chat/create#chat/create-role" target="_blank">OpenAI Chat</a> for more about message role.
    ```jinja
    system:
    You are a chatbot having a conversation with a human.

    user:
    {{question}}
    ```
- how to consume chat history in prompt.
    ```jinja
    {% for item in chat_history %}
    user:s
    {{item.inputs.question}}
    assistant:
    {{item.outputs.answer}}
    {% endfor %}
    ```

## Tools used in this flow
- LLM tool
- Python tool
