# Streamlit Dashboard for Evaluating daily symptomps

This dashboard interacts with patients from the Princess Maxima Center of Pediatric Oncology. 
It begins with a basic set of questions, that is easy to interact with, to evaluate daily symptomps and establish the current state of the patient. There is potential to make the questions more tailored to the needs of the patient.
Combined with the patients background and similar case studies, context is provided downstream.
At last, a Vector Store is used to provide symptom information from literature. ( not implemented )

The dashboard serves two goals:
1. To be a compassionate companion for the children that provides emotional support, reassurance, and age-appropriate coping strategies.
2. Alert doctors in case of progressively worsening symptoms and provide a summary

### General Architecture

![google_hackathon](https://github.com/zsolthubai/maxima-google/assets/145662011/c00564f7-77b9-4748-97f4-a849f73710e9)


### Installation and usage:
To get started, you'll need to ensure you have the necessary tools and configurations in place.

**Prerequisites:**
- Vertex AI by the Google Cloud Platform.
- LangChain: You'll need the langchain-google-vertexai Python package installed. This package allows LangChain to interact with Vertex AI's models.
- Google Cloud SDK: Ensure you have the google-cloud-sdk installed and configured. This enables command-line interaction with Google Cloud services.
Authentication: Proper authentication is required for accessing Vertex AI services.

**Resources:**
For detailed instructions on setting up and using LangChain with Vertex AI, refer to the following resources:
- https://python.langchain.com/docs/expression_language/get_started/
- https://python.langchain.com/docs/integrations/llms/google_vertex_ai_palm/

### How to use:
1. Open Streamlit Dashboard by running: streamlit run streamlit_app.py
2. Select the Patient or Doctor tab (to be implemented).
3. Enter Patient name on the left.
4. Answer questionnaire (with sliders & emoji for children)
    - All information is combined in a prompt and context from similar case studies and vector store are added.
5. Advice is generated using above prompt
6. Summary of conversation and advice is stored for the doctor.
7. We assume that BigQuery is supplied with patient data from a different frontend.
8. We also assume that BigQuery is the data warehouse for chat history.
