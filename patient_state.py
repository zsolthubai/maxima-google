import streamlit as st

class patient_state:
     

     col1, col2, col3, col4, col5 = st.columns(5)
     with col1:
          btn_happy = st.button(":smiley:")
     with col2:
          btn_neutral = st.button(":expressionless:")
     with col3:
          btn_unhappy = st.button(":disappointed:")
     with col4:
          btn_sad = st.button(":sob:")
     with col5:
          btn_urgent_help = st.button(":ambulance:")

     if btn_happy:
          state = "I feel well and am able to do my usual activities."
     elif btn_neutral:
          state="I feel okay but have some side effects that interfere with my daily activities a little."
     elif btn_unhappy:
          state="I don't feel well and have side effects that make it difficult to do many of my usual activities."
     elif btn_sad:
          state="I feel very unwell and am unable to do most of my usual activities. I need help with basic needs."
     elif btn_urgent_help:
          state="I feel terrible and need immediate medical attention"
     
     pain_level = st.slider('If you are feeling pain, how worse is it ?', 0, 10)
     nausea_level = st.slider('How is your nausea?', 0, 10)
     anxiety_level = st.slider('Do you feel anxious?', 0, 10)