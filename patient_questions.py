import streamlit as st

class pain_questionaire:
    def getquestions():
         st.slider('How strong is your pain ?', 0, 5)
         st.radio(
                "Is it constant or does it come and go?",
                ["It comes and go", "Its comes and goes but last for more than 30 minutes"],index=None,)
         
         st.radio( "What makes your pain worse?",
                ["Certain movements or activities?",
                "Coughing or deep breathing?",
                "Touching the area?",
                "Stress or anxiety?"],index=None,)
         st.radio( "What makes your pain better?",
                ["Rest?",
                "Medication?",
                "Hot/cold packs?",
                "Certain positions or activities?"],index=None,)
         
class nausea_questionaire:
     def getquestions():
           st.slider('How frequently do feel nauseated', 0, 5)
           st.slider('Did you vomit today?', 0, 1)
           st.slider('Do you feel like eating?', 0, 5)
           st.slider('Are you able to drink', 0, 5)

class anxiety_questionaire:
      def getquestions():
           st.slider('I am losing hope in the fight against my illness', 0, 5)
           st.slider('I get emotional support from my family', 0, 5)
           st.slider('I worry that my condition will get worse', 0, 5)
           st.slider('I am forced to spend time in bed', 0, 5)
           