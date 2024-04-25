import documents
from langchain.memory import ConversationBufferMemory
import streamlit as st
from utils import bq
from langchain_google_vertexai import ChatVertexAI
from langchain.chains import ConversationChain
import patient_questions as pq


response_keys={"patient_state":"How are you feeling today?",
               "pain_slider":"How strong is your pain ?",
               "pain_radio1":"What makes your pain worse?",
               "pain_radio2":"What makes your pain better?"}

@st.cache_resource(show_spinner=False)
def LLM_init():
    # memory = ConversationBufferMemory(memory_key="chat_history")
    llm = ChatVertexAI(model_name="gemini-pro", convert_system_message_to_human=False)
    memory = ConversationBufferMemory()
    chain = ConversationChain(llm=llm, memory=memory)
    return chain


st.title("🚀 Welcome to MaximAI, an AI powered assitant application")

if "id_submitted" not in st.session_state:
    st.session_state["id_submitted"] = False
if not st.session_state["id_submitted"]:
    st.info("🔗 Please provide patient identification")

with st.sidebar.form("form_name"):
    patient_id = st.sidebar.text_input("Patient ID")
    patient_name = st.sidebar.text_input("Patient full name")
    submitted = st.form_submit_button("Submit")
if submitted:
    st.session_state["id_submitted"] = True
    st.info(f"Retreiving info for patient {patient_id}, {patient_name}")

if st.session_state["id_submitted"]:
    patient_info_prompt = bq.get_patient_records(patient_id, patient_name)

    if "clicked" not in st.session_state:
        st.session_state.clicked = False

    def click_button():
        st.session_state.clicked = True

    st.info(f'How are you feeling today {patient_name.split(" ")[0]}?')
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
        patient_state = "I feel well and am able to do my usual activities."
        st.session_state["patient_state"] = patient_state
    elif btn_neutral:
        patient_state = "I feel okay but have some side effects that interfere with my daily activities a little."
        st.session_state["patient_state"] = patient_state
    elif btn_unhappy:
        patient_state = "I don't feel well and have side effects that make it difficult to do many of my usual activities."
        st.session_state["patient_state"] = patient_state
    elif btn_sad:
        patient_state = "I feel very unwell and am unable to do most of my usual activities. I need help with basic needs."
        st.session_state["patient_state"] = patient_state
    elif btn_urgent_help:
        patient_state = "I feel terrible and need immediate medical attention"
        st.session_state["patient_state"] = patient_state

    if st.session_state.clicked:
        # anxiety_questionaire = pq.anxiety_questionaire.getquestions()
        # nausea_questionaire = pq.nausea_questionaire.getquestions()
        # pain_questionaire = pq.pain_questionaire.getquestions()
        
        if "pain_slider" not in st.session_state:
            st.session_state["pain_slider"] = ""
        pain_slider = st.slider('How strong is your pain ?', 0, 5)
        if pain_slider:
            st.session_state["pain_slider"] = pain_slider
        
        if "pain_radio1" not in st.session_state:
            st.session_state["pain_radio1"] = ""
        pain_radio1 = st.radio( "What makes your pain worse?",
                ["Certain movements or activities?",
                "Coughing or deep breathing?",
                "Touching the area?",
                "Stress or anxiety?"],index=None)
        if pain_radio1:
            st.session_state["pain_radio1"] = pain_radio1

        if "pain_radio2" not in st.session_state:
            st.session_state["pain_radio2"] = ""
        pain_radio2 = st.radio(
            "What makes your pain better?",
            [
                "Rest",
                "Medication",
                "Hot/cold packs",
                "Certain positions or activities",
            ],
            index=None,
        )
        if pain_radio2:
            st.session_state["pain_radio2"] = pain_radio2

            template = documents.instruction
            llm_chain = LLM_init()
            prompt = template.format(patient_info_prompt, "/n".join(f"Question:{question}, Answer:{st.session_state[element]}" for element, question in response_keys.items()) )
            msg = llm_chain(prompt)
            st.info(msg["response"])

        # st.session_state.messages.append({"role": "assistant", "content": "Hi How can I help?"})
        # st.chat_message("assistant").write(msg)
