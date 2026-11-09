from langgraph.graph import StateGraph,START,END,MessagesState
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage
from typing import TypedDict
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

# class nodeState(TypedDict):
#     usermsg:str
#     assistantmsg:str

model=ChatOpenAI(model="gpt-4o-mini")

# def user_response(state: MessagesState):
#     cleaned = state["usermsg"].strip()
#     return {"usermsg": cleaned}

def assistant_response(state:MessagesState):
    reply=model.invoke(state["messages"])
    return {"messages": [reply]}


graph=StateGraph(MessagesState)
# graph.add_node("user_response",user_response)
graph.add_node("assistant_response",assistant_response)

graph.add_edge(START,"assistant_response")
graph.add_edge("assistant_response",END)

checkpointer=MemorySaver()
config={"configurable": {"thread_id": "1"}}

app=graph.compile(checkpointer=checkpointer)
app.invoke({"messages": [HumanMessage(content="Hello! My name is devanshi")]}, config)
result=app.invoke({"messages": [HumanMessage(content="what is my name?")]}, config)
print(result["messages"][-1].content)
