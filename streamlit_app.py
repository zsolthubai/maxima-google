import documents
from langchain.llms import VertexAI
from langchain import PromptTemplate, LLMChain
from langchain.memory import ConversationBufferMemory
import streamlit as st
from utils import bq
from langchain_google_vertexai import ChatVertexAI
from langchain.chains import ConversationChain

@st.cache_resource(show_spinner=False)
def LLM_init():
    # memory = ConversationBufferMemory(memory_key="chat_history")
    llm = ChatVertexAI(model_name="gemini-pro", convert_system_message_to_human=False)
    memory = ConversationBufferMemory()
    chain = ConversationChain(llm=llm, memory=memory)
    return chain

st.title(f'🦜🔗Hi! Welcome to the Maxima AI ChatBot.')

if 'id_submitted' not in st.session_state:
    st.session_state['id_submitted'] = False
    
if not st.session_state['id_submitted']:
    st.info('🦜🔗 Please provide patient identification')

with st.sidebar.form("form_name"):
    patient_id = st.sidebar.text_input('Patient ID')
    patient_name = st.sidebar.text_input('Patient full name')
    submitted = st.form_submit_button("Submit")
if submitted:
    st.session_state['id_submitted'] = True
    st.info(f"Retreiving info for patient {patient_id}, {patient_name}")

if st.session_state['id_submitted']:
    
    patient_info_prompt = bq.get_patient_records(patient_id, patient_name)
    
    if 'clicked' not in st.session_state:
        st.session_state.clicked = False

    def click_button():
        st.session_state.clicked = True
    
    st.info('How are you feeling today?')
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        btn_happy = st.button(":smiley:", on_click=click_button)
    with col2:
        btn_neutral = st.button(":expressionless:", on_click=click_button)
    with col3:
        btn_unhappy = st.button(":disappointed:", on_click=click_button)
    with col4:
        btn_sad = st.button(":sob:", on_click=click_button)
    with col5:
        btn_urgent_help = st.button(":ambulance:", on_click=click_button)

    if btn_happy:
        patient_state="I feel well and am able to do my usual activities."
        st.session_state['patient_state']=patient_state
    elif btn_neutral:
        patient_state="I feel okay but have some side effects that interfere with my daily activities a little."
        st.session_state['patient_state']=patient_state
    elif btn_unhappy:
        patient_state="I don't feel well and have side effects that make it difficult to do many of my usual activities."
        st.session_state['patient_state']=patient_state
    elif btn_sad:
        patient_state="I feel very unwell and am unable to do most of my usual activities. I need help with basic needs."
        st.session_state['patient_state']=patient_state
    elif btn_urgent_help:
        patient_state="I feel terrible and need immediate medical attention"
        st.session_state['patient_state']=patient_state
        
    if st.session_state.clicked:
        
        st.info(st.session_state['patient_state'])
    
        # if "messages" not in st.session_state:
        #     st.session_state["messages"] = [{"role": "assistant", "content": "Hi How can I help?"}]

        #"st.session_state:", st.session_state.messages

        # for msg in st.session_state.messages:
            # st.chat_message(msg["role"]).write(msg["content"])

        #if prompt := st.chat_input():

        # st.session_state.messages.append({"role": "user", "content": "Hi How can I help?"})
        # st.chat_message("user").write(prompt)
        # with st.spinner('Preparing'):
        template =  documents.instructions
        llm_chain = LLM_init()
        prompt = template.format(patient_info_prompt, patient_state)
        msg = llm_chain(prompt)
        # st.info(msg["text"])
        # promptllm = PromptTemplate(template=template, input_variables=["patient_data"])
        # st.write(msg['response'])
        st.write(msg)

        # st.session_state.messages.append({"role": "assistant", "content": "Hi How can I help?"})
        # st.chat_message("assistant").write(msg)