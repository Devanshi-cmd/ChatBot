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

def stream_reply(user_input,thread_id):
    config={"configurable":{"thread_id": thread_id}}
    for chunk,metadata in app.stream(
        {"messages":[HumanMessage(content=user_input)]},
        config=config,
        stream_mode="messages"
    ):
        yield chunk.content



