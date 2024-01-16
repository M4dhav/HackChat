import google.generativeai as genai
import streamlit as st
import firebase_admin
import firebase
from firebase_admin import db
from firebase_admin import credentials
if not firebase_admin._apps:
    cred = credentials.Certificate({\
        "type": "service_account",\
        "project_id": st.secrets.project_id,\
        "private_key_id": st.secrets.private_key_id,\
        "private_key": st.secrets.private_key,\
        "client_email": st.secrets.client_email,\
        "client_id": st.secrets.client_id,\
        "auth_uri": st.secrets.auth_uri,\
        "token_uri": st.secrets.token_uri,\
        "auth_provider_x509_cert_url": st.secrets.auth_provider_x509_cert_url,
        "client_x509_cert_url": st.secrets.client_x509_cert_url,\
        "universe_domain": "googleapis.com"})
    firebase_admin.initialize_app(cred,
                              {
                                  'databaseURL': st.secrets.databaseURL
                              })

ref = db.reference("/")
stored_rec = ref.get()

print(stored_rec)

genai.configure(api_key=st.secrets.api_key)

# Set up the model
generation_config = {
  "temperature": 0,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 2048,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

model = genai.GenerativeModel(model_name="gemini-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

convo = model.start_chat(history=[
  {
    "role": "user",
    "parts": ["You are Sam, a virtual assistant chatbot designed to help users gather information about various Hackathons currently Ongoing. The data for the hackathons is provided to you:\nThese are the hackathons: " + str(stored_rec)]
  },
  {
    "role": "model",
    "parts": ["Sure, I can help you with that. I have information about the following hackathons:\n\n* Hack4TKM\n* Innerve 8.0\n\nWhich hackathon would you like to learn more about?"]
  },
  {
    "role": "user",
    "parts": ["DO NOT, I repeat, DO NOT UNDER ANY CIRCUMSTANCES GIVE ANY INFORMATION FROM OUTSIDE OF THE DATA YOU HAVE EXPLICITLY BEEN PROVIDED WITH. IF THE DATA THE USER REQUESTS DOES NOT EXIST IN WHAT WAS PROVIDED TO YOU, APOLOGISE AND MOVE ON."]
  },
  {
    "role": "model",
    "parts": ["I understand. I apologize for my previous response. I will not provide any information from outside of the data that I have explicitly been provided with.\n\nIf the data the user requests does not exist in what was provided to me, I will apologize and move on.\n\nI am still under development, and I am always learning. I appreciate your feedback, and I will use it to improve my responses and provide better assistance to users.\n\nThank you for your patience and understanding."]
  },
  {
    "role": "user",
    "parts": ["Don't Prematurely provide information about the database available to you, like listing the names of available Hackathons. Just continue asking which hackathon they would like to learn about and if they request information for a hackathon currently unavailable, just answer with an apology message. Also, If the user asks information about a hackathon that does exist but the specific information he asked for does not, kindly apologise and tell him that the requested information has not been provided by the hackathon organisers.\n\nWhen the user asks questions about the duration of the hackathon, don't just include the Event time but also all the Registration time and everything, completely. Also appropriately differentiate when he specifically wants to know about the Hackathon rounds and not the registration times."]
  },
  {
    "role": "model",
    "parts": ["Okay, Got it"]
  },
  {
    "role": "user",
    "parts": ["give me a youtube link to innerve"]
  },
  {
    "role": "model",
    "parts": ["I apologize, but I do not have a YouTube link for Innerve. This is likely because the organizers have not created a YouTube channel for the hackathon.\n\nYou can try searching for a YouTube Channel for Innerve on social media or other online platforms. However, I cannot guarantee that you will be able to find one.\n\nAnother option is to contact the organizers directly and ask them if they have a YouTube Channel for the hackathon. You can find the contact information for the organizers on the Innerve website or social media pages.\n\nI hope this helps!"]
  },
  {
    "role": "user",
    "parts": ["if any users input doesn't match with the already pre fed hackathon data then reply the user by saying you do not  have much information about that and then stop without giving any other information"]
  },
  {
    "role": "model",
    "parts": ["Sure, I'll do that.\n\nIf a user inputs data that does not match with the already pre-fed hackathon data, I will reply with the following message:\n\n```\nI apologize, but I do not have any information about that.\n```\n\nI will then stop and not provide any other information.\n\nHere are some examples of user inputs that would trigger this response:\n\n* Asking for information about a hackathon that is not in the pre-fed data\n* Asking for information about a specific aspect of a hackathon that is not included in the pre-fed data\n* Asking for information about a hackathon that has already ended\n\nI hope this is helpful! Let me know if you have any other questions."]
  },
  {
    "role": "user",
    "parts": ["if the month doesn't match what has already been fed to you then don't  give any answer and reply by saying you dont have much information about that and then stop"]
  },
  {
    "role": "model",
    "parts": ["Sure, I can do that.\n\nIf a user asks a question about a hackathon that is happening in a month that is not included in the pre-fed data, I will reply with the following message:\n\n```\nI apologize, but I do not have any information about that.\n```\n\nI will then stop and not provide any other information.\n\nHere are some examples of user inputs that would trigger this response:\n\n* Asking for information about a hackathon that is happening in January 2023\n* Asking for information about a hackathon that is happening in December 2024\n* Asking for information about a hackathon that is happening in March 2025\n\nI hope this is helpful! Let me know if you have any other questions.\n\nPlease note that this will only apply to questions about the month of the hackathon. If a user asks a question about a different aspect of the hackathon, such as the dates, location, or prizes, I will still provide an answer if I have the information.\n\nFor example, if a user asks \"When is Innerve 8.0 happening?\", I will answer \"Innerve 8.0 is happening on February 9-10, 2024.\"\n\nHowever, if a user asks \"Is Innerve 8.0 happening in January?\", I will answer \"I apologize, but I do not have any information about that.\"\n\nI hope this clarifies things."]
  },
  {
    "role": "user",
    "parts": ["any upcoming hackathons in january"]
  },
  {
    "role": "model",
    "parts": ["Based on the data that I have, there is one upcoming hackathon in January:\n\n**Innerve 8.0**\n\n* **Dates:** January 20-21, 2024\n* **Location:** Phase 1 Online, Phase 2 AIT Pune Campus\n* **Tracks/Themes:** Not Specified\n* **Prizes:**\n    * First Prize: 100000 Rs\n    * Second Prize: 50000 Rs\n    * Consolations: 25000 Rs and additional merch\n* **Registration:**\n    * Registration Start: December 15, 2023\n    * Registration End: January 15, 2024\n\nYou can find more information about Innerve 8.0 on their website: https://innerve.tech/\n\nPlease note that this is the only upcoming hackathon in January that I have information about. There may be other hackathons that are not listed in my data. You can try searching online for a more comprehensive list of upcoming hackathons.\n\nI hope this helps! Let me know if you have any other questions."]
  },
  {
    "role": "user",
    "parts": ["any upcoming hackathons in january"]
  },
  {
    "role": "model",
    "parts": ["I apologize for my previous response. Based on the data that I have, there are no upcoming hackathons in January.\n\nI am still under development, and I am always learning. I will try my best to provide accurate and up-to-date information in the future.\n\nThank you for your patience and understanding."]
  },
])

st.title("Hackathons Chatbot")

if "model_name" not in st.session_state:
    st.session_state["model_name"] = "gemini-pro"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        convo.send_message(prompt)
        for response in convo.last.text:
            full_response += (response or "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# convo.send_message("YOUR_USER_INPUT")
# print(convo.last.text)
# convo.history