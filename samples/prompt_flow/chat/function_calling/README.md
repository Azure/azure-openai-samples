# Use Functions with Chat Models

This flow covers how to use the LLM tool chat API in combination with external functions to extend the 
capabilities of GPT models. 

`functions` is an optional parameter in the <a href='https://platform.openai.com/docs/api-reference/chat/create' target='_blank'>Chat Completion API</a> which can be used to provide function 
specifications. The purpose of this is to enable models to generate function arguments which adhere to the provided 
specifications. Note that the API will not actually execute any function calls. It is up to developers to execute 
function calls using model outputs. 

If the `functions` parameter is provided then by default the model will decide when it is appropriate to use one of the 
functions. The API can be forced to use a specific function by setting the `function_call` parameter to 
`{"name": "<insert-function-name>"}`. The API can also be forced to not use any function by setting the `function_call` 
parameter to `"none"`. If a function is used, the output will contain `"finish_reason": "function_call"` in the 
response, as well as a `function_call` object that has the name of the function and the generated function arguments. 
You can refer to <a href='https://github.com/openai/openai-cookbook/blob/main/examples/How_to_call_functions_with_chat_models.ipynb' target='_blank'>openai sample</a> for more details.


## What you will learn

In this flow, you will learn how to use functions with LLM chat models and how to compose function role message in prompt template.

## Tools used in this flow
- LLM tool
- Python tool

## References
- <a href='https://github.com/openai/openai-cookbook/blob/main/examples/How_to_call_functions_with_chat_models.ipynb' target='_blank'>OpenAI cookbook example</a>
- <a href='https://openai.com/blog/function-calling-and-other-api-updates?ref=upstract.com' target='_blank'>OpenAI function calling announcement</a> 
- <a href='https://platform.openai.com/docs/guides/gpt/function-calling' target='_blank'>OpenAI function calling doc</a>
- <a href='https://platform.openai.com/docs/api-reference/chat/create' target='_blank'>OpenAI function calling API</a>
