from typing import List, Tuple

from langgraph.prebuilt import create_react_agent
from langchain.agents.format_scratchpad import format_to_openai_function_messages
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from langchain.utilities.tavily_search import TavilySearchAPIWrapper
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI

# Create custome the tool 
search = TavilySearchAPIWrapper()
description = """"A search engine optimized for comprehensive, accurate, \
and trusted results. Useful for when you need to answer questions \
about current events or about recent information.  \
Input should be a search query. \
If the user query is asking about something that you don't know about, \
you should probably use this tool to see if that can provide any information."""
tavily_tool = TavilySearchResults(api_wrapper=search, description=description)

tools = [tavily_tool]

llm = ChatGoogleGenerativeAI(temperature=0, model="gemini-2.5-flash")

prompt = ChatPromptTemplate.from_messages(
    [
      # MessagesPlaceholder(variable_name="chat_history"),
        (user, "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

llm_with_tools = llm.bind(functions=tools)

agent = (
    {
        "input": lambda x: x["input"],
        "agent_scratchpad": lambda x: format_to_openai_function_messages(
            x["intermediate_steps"]
        ),
    }
    | prompt 
    | llm_with_tools
    | OpenAIFunctionsAgentOutputParser()
)

agent_executor = create_react_agent(llm, tools)
#AgentExecutor(agent=agent, tools=tools, verbose=True)

agent_executor.invoke({"input": "Who is the head of DeepMind"})