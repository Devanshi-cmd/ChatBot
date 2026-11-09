import uuid
import streamlit as st
from langchain_core.messages import HumanMessage
from app import app, stream_reply
st.title("My Chatbot")

#we are using history because here each time streamlit runs it runs the entire script from start so prev msges are erased here
if "thread_id" not in st.session_state:
    st.session_state.thread_id=str(uuid.uuid4())
if "history" not in st.session_state:
    st.session_state.history = []

for role,text in st.session_state.history:
    with st.chat_message(role):
        st.write(text)


user_input=st.chat_input("Type your message here...")

if user_input:
    st.session_state.history.append(("user",user_input))
    with st.chat_message("user"):
        st.write(user_input)

    # config={"configurable":{"thread_id": st.session_state.thread_id}}
    # result=app.invoke({"messages":[HumanMessage(content=user_input)]},config)
    # assistantreply=result["messages"][-1].content

    # st.session_state.history.append(("assistant",assistantreply))

    with st.chat_message("assistant"):
        reply = st.write_stream(stream_reply(user_input, st.session_state.thread_id))
    st.session_state.history.append(("assistant", reply))
