from langchain.llms import VertexAI
from langchain import PromptTemplate, LLMChain
from langchain.memory import ConversationBufferMemory
import streamlit as st
from utils import bq

@st.cache_resource(show_spinner=False)
def LLM_init():
    template = """
    Your name is Dr. AI. You are an asistant to a doctor treating childen with cancer.
    {chat_history}
        Human: {human_input}
        Chatbot:"""

    promptllm = PromptTemplate(template=template, input_variables=["chat_history","human_input"])
    memory = ConversationBufferMemory(memory_key="chat_history")
    
    llm_chain = LLMChain(
        prompt=promptllm, 
        llm=VertexAI(), 
        memory=memory, 
        verbose=True
    )
    
    return llm_chain

st.title(f'🦜🔗Hi! Welcome to the Maxima AI ChatBot.')
button_pressed = False

patient_id = st.sidebar.text_input('Patient ID')
patient_name = st.sidebar.text_input('Patient full name')


if (not patient_id) and (not patient_name):
    st.info('🦜🔗 Please provide patient identification')
    
if patient_id or patient_name:
    
    st.info(bq.get_patient_records(patient_id, patient_name))
    
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": f"Hi, my name is Dr. AI. I am your assistant, how can I help you with patient {patient_info}?"}]
    
    for msg in st.session_state.messages:
       st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input():

        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        # with st.spinner('Preparing'):
        llm_chain = LLM_init()
        msg = llm_chain.predict(human_input=prompt)

        #st.write(msg)

        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.chat_message("assistant").write(msg)