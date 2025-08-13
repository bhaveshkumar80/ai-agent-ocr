from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.messages import HumanMessage, AIMessage
from tools import OCR_TOOL, RAG_TOOL, WEATHER_TOOL, NO_TOOL
from store_chats import init_db, store_message
import streamlit as st
import os
import uuid

load_dotenv()
init_db()

# --- Streamlit UI ---
st.set_page_config(page_title="AI Chatbot", page_icon="🤖")
st.title("🤖 AI Chatbot with Tools")

#load LLM
llm = ChatOllama(model="llama3.1:8b")


#define prompt
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are a helpful AI assistant with access to the following tools:

            1. collect_weather_data - Retrieves current and forecasted weather details (temperature, humidity, precipitation, wind) for a given location from weather.com.
            2. Extract_info_from_files - Extracts text from image, PDF, or DOCX files provided via a file path, converting them into plain text.(File path should be as it is)
            3. retrieve_document - Searches and retrieves relevant information from a medical document database in response to health or medicine-related queries.
            4. NoToolNeeded - Use your own knowledge to answer the query.

            Rules:
            - If query is related to chat history, answer from chat history and use no tool call.
            - Select the tool best suited for the task based on its description.
            - Provide only the required input parameters.
            - Do not modify the input path, given for extract_info_from_files tool.
            - Do not fabricate information; rely on tool outputs for facts.
            - Never mention tool name in the final output
            """,
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{query}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)


tools = [OCR_TOOL, RAG_TOOL, WEATHER_TOOL, NO_TOOL]

#Tool calling agent to call specific tool
agent = create_tool_calling_agent(
    llm=llm,
    prompt=prompt,
    tools=tools
)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

#unique session id
session_id = str(uuid.uuid4())

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_query = st.chat_input("Type your message...", accept_file=True, file_type=['.jpg', '.jpeg', '.png', '.docx', '.pdf'])


if user_query:
    if len(user_query.files) != 0:
        file_path = None
        uploaded_file = user_query.files[0]
        print("Uploaded FIle: ", uploaded_file)
        if uploaded_file is not None:
            temp_dir = "input_files/"
            file_path = os.path.join(temp_dir, uploaded_file.name)
            print("file path: ", file_path)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            # Attach file path to query for backend processing
            updated_user_query = user_query.text  + f"\n\n[File path: {file_path}]"
            user_query.text = user_query.text + f": {uploaded_file.name}"
    else:
        updated_user_query = user_query.text

    # Display user message
    st.chat_message("user").markdown(user_query.text)
    st.session_state.messages.append({"role": "user", "content": user_query.text})

    # Run the agent
    raw_response = agent_executor.invoke({
        "query": updated_user_query,
        "chat_history": st.session_state.chat_history
    })

    ai_reply = raw_response["output"]

    # Display AI reply
    st.chat_message("assistant").markdown(ai_reply)
    st.session_state.messages.append({"role": "assistant", "content": ai_reply})

    # Update memory + store in DB
    st.session_state.chat_history.append(HumanMessage(content=user_query.text))
    st.session_state.chat_history.append(AIMessage(content=ai_reply))
    store_message(session_id, updated_user_query, ai_reply)
