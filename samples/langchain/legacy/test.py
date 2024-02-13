from langchain.llms import OpenAIChat
import os
from dotenv import load_dotenv
from langchain.agents import load_tools
from langchain.agents import initialize_agent, Tool
from langchain.utilities import BingSearchAPIWrapper
load_dotenv()

# Next, let's load some tools to use. Note that the `llm-math` tool uses an LLM, so we need to pass that in.

llm = OpenAIChat(temperature=0, 
                  engine='gpt-35-turbo')

# Next, let's load some tools to use. Note that the `llm-math` tool uses an LLM, so we need to pass that in.
tools = load_tools(["bing-search", "llm-math"], llm=llm)

# Finally, let's initialize an agent with the tools, the language model, and the type of agent we want to use.
agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True, return_intermediate_steps=True)

# Now let's test it out!
response = agent({"input":"Is BMW X1 2023 more affortable than Tesla model 3 2023? List prices for both cars."})
print(response['output'])