# import nest_asyncio
# nest_asyncio.apply()
# from concurrent.futures import ThreadPoolExecutor
from langchain_classic.tools import Tool
from langchain_core.prompts import PromptTemplate
from langchain_classic.agents import create_react_agent,AgentExecutor
from whatsapp_automation.open_whatsapp import send_whatsapp_message
from langchain_classic.memory import ConversationBufferMemory
from langchain_groq import ChatGroq
from tavily import TavilyClient
from duckduckgo_search import DDGS
from rag import retriever
from dotenv import load_dotenv
import asyncio
import state
import os
# import threading

load_dotenv()


llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)

tavily_client = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)

def web_search(query):
    ddg_results = ""
    tavily_results = ""

    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query,max_results=3))

        if results:
            ddg_results = "DuckDuckGo results\n"
            for r in results:
                ddg_results += f"Title: {r['title']}\n"
                ddg_results += f"Summary: {r['content']}\n\n"
    except:
        pass

    try:
        response = tavily_client.search(query,max_results=3)
        if response['results']:
            tavily_results = "Tavily results\n\n"
            for r in response["results"]:
                tavily_results += f"Title: {r['title']}\n"
                tavily_results += f"Summary: {r['content']}\n\n"
    except:
        pass

    if ddg_results and tavily_results:
        return ddg_results + "\n" + tavily_results
    elif ddg_results:
        return ddg_results
    elif tavily_results:
        return tavily_results
    else:
        return "No Result found from any search engine"
    
def calculate(expression):
    try:
        return str(eval(expression))
    except:
        return "invalid Expression"

def search_docs(query):
    if state.pdf_uploaded:
        results = state.pdf_retriever.invoke(query)
    else:

        results = retriever.invoke(query)
    return "\n".join([r.page_content for r in results])

def whatsapp_tool(query):
    print(f"Query recived:{query}")
    parts = query.split("|")
    print(f"Parts: {parts}")
    contact_name = parts[0].strip()
    message = parts[1].strip()
    return send_whatsapp_message(contact_name,message)

    # result = [None]

    # def run():
    #     result[0] = send_whatsapp_message(contact_name,message)
    # thread = threading.Thread(target=run)
    # thread.start()
    # thread.join(timeout=60)

    # return result[0] or "message sent!"




#Trying to fix event loop 
    # with ThreadPoolExecutor() as executor:
    #     future = executor.submit(
    #         asyncio.run,
    #         send_whatsapp_message(contact_name,message)
    #     )
    #     return future.result()

    # return asyncio.run(send_whatsapp_message(contact_name,message))
    


tools = [
    Tool(
        name="calculator",
        func=calculate,
        description="use this to calculate math expression input should be a math expression like '25 * 0.25'"
    ),
    Tool(
        name="DocsSearch",
        func=search_docs,
        description="use this to search company policy documents. input should be a question about compant policies"
    ),
    Tool(
        name="WebSearch",
        func=web_search,
    description="Use this to search the internet for current information not available in company documents. Input should be a search query."
    ),
    Tool(
        name="send_whatsapp_message",
        func=whatsapp_tool,
        description="Use this to send whatsapp message. input format: 'contact_name|message"
    )
]

template = """Answer the following questions as best you can.

You have access to the following tools:
{tools}

Previous conversation:
{chat_history}

IMPORTANT RULES:
- ALWAYS use a tool to answer, even if you think you know the answer
- NEVER use Action: None
- If question was asked before, use DocumentSearch again to confirm
- After getting Observation, IMMEDIATELY write Final Answer
- Do NOT search again if you already have the answer

Use the following format:
Question: the input question you must answer
Thought: think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
Thought: I now know the final answer
Final Answer: the final answer to the original question

Question: {input}
Thought: {agent_scratchpad}
"""

prompt = PromptTemplate.from_template(
    template
)

agents = create_react_agent(
    llm=llm,
    tools=tools,
    prompt=prompt
)

memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=False
)

agent_executor = AgentExecutor(
    agent=agents,
    memory=memory,
    tools=tools,
    verbose=True,
    max_iterations=7,
    handle_parsing_errors=True
)