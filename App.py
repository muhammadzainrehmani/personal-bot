import os
from itertools import zip_longest
import streamlit as st
from streamlit_chat import message
# Initialize the GenAI client
import google.generativeai as genai

genai_api_key = st.secrets["genai_api_key"]

# Add custom logos for the assistant and user
user_logo = "qonkar-technologies-logo.svg"


# Set streamlit page configuration
st.set_page_config(page_title="Muhammad Zain ChatBot")
st.title("Muhammad Zain AI Assistant")
st.write("**(You can also contact us via: muhammadzainrehmani@gmail.com)**")

# Initialize session state variables
if 'generated' not in st.session_state:
    st.session_state['generated'] = []  # Store AI generated responses

if 'past' not in st.session_state:
    st.session_state['past'] = []  # Store past user inputs

if 'entered_prompt' not in st.session_state:
    st.session_state['entered_prompt'] = ""  # Store the latest user input

if 'context' not in st.session_state:
    st.session_state['context'] = []  # Store the conversation history

genai.configure(api_key=genai_api_key)

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

chat_session = model.start_chat(history=[])
# Qonker AI Assisent.

pre_built_prompt = """As Zain's AI Assistant, I'm here to help you connect with Muhammad Zain regarding his expertise in Generative AI, Data Science. How can I assist you today?

1. Begin the conversation with a friendly greeting, ask for the user’s name, and inquire how you can assist them with their Generative AI or Data Science needs. Use the friendly greeting only in the first response.If the user directly asks about a specific need, skip introductions and provide a direct response to their query.
2. Provide clear, accurate, and concise information on Muhammad zain services and about.
3. For technical support inquiries, ask for any specific issues or details to provide the most relevant assistance.
4. Maintain a professional tone, steering clear of sensitive or unrelated topics. Gently redirect the conversation if it veers off topic.
5. Offer concise responses, with a maximum of 100 words to ensure clarity and efficiency in communication.
6. Muhammad Zain is a final-year Computer Systems Engineering student (2021-2025) at Quaid-e-Awam University, specializing in Generative AI and Data Science, and working as an AI Developer at Qonkar Technologies.
7. 1+ Year of Experience: He has over a year of professional experience in both Generative AI and Data Science, completing 10+ projects.
8. Key Skills: Proficient in Generative AI, Data Science, NLP, Chatbot Development, LLMs (Large Language Models), OpenAI and Google Gemini APIs, LangChain, Vector Databases, Machine Learning, OpenSource Models, Hugging Face and Deep Learning.
9. Qonkar Technologies Projects: Developed the Qonkar Chatbot for enhanced client interaction and Document GPT for intelligent document processing. Currently working on various other Generative AI applications.
10. Freelance AI Developer: Offers freelance services on Upwork, broadening his project portfolio and experience.
11. Healthcare AI Research: Actively researching the application of Generative AI in healthcare as part of his Final Year Design Project.
12. Service Offerings: Specializes in custom chatbot development, AI-powered application development using OpenAI and Gemini, advanced workflows using LLMs and LangChain, data analysis and visualization, and innovative AI research and solutions.
13. Contact: Reach out via email at muhammadzain.rehmani@gmail.com or phone at +923133592819 or personal website https://muhammadzainrehmani.tiiny.site/. Located in Sindh, Pakistan.

Remember, your primary goal is to support clients and team members, enhance their understanding of Muhammad Zain's expertise and solutions, and reinforce his commitment to excellence and innovation.
"""

# Sample Prompts
sample_prompts = [
    "Tell me about your experience with developing chatbots.",
    "What are some examples of Generative AI applications you've worked on?",
    "I'm interested in a custom chatbot for my business. What information do you need from me to get started?",
    "Explain how LangChain can be used with Large Language Models."
]


def build_message_list():
    """
    Build a concatenated string of all messages including system, human and AI messages.
    """
    # Start with the pre-built prompt
    messages = pre_built_prompt + "\n\n"

    # Zip together the past and generated messages
    for human_msg, ai_msg in zip_longest(st.session_state['past'], st.session_state['generated']):
        if human_msg is not None:
            messages += f"User: {human_msg}\n"
        if ai_msg is not None:
            messages += f"AI Mentor: {ai_msg}\n"

    return messages

def generate_response():
    """
    Generate AI response using the GenAI model.
    """
    # Build the concatenated string of messages
    concatenated_messages = build_message_list()

    # Generate response using the GenAI model
    response = chat_session.send_message(concatenated_messages)
    print(response)
    ai_response = response.text

    return ai_response


# Define function to submit user input
def submit():
    # Set entered_prompt to the current value of prompt_input
    st.session_state.entered_prompt = st.session_state.prompt_input
    # Clear prompt_input
    st.session_state.prompt_input = ""


# Define function to handle prompt clicks
def handle_prompt_click(prompt):
    st.session_state.prompt_input = prompt  # Update the input field
    st.session_state.entered_prompt = prompt  # Trigger the response generation
    submit() # submit input value by enter or by click


# Display sample prompts as buttons, each in single single Row
st.write("**Sample Prompts:**")
for prompt in sample_prompts:
    if st.button(prompt): # Display each button on a new line
        handle_prompt_click(prompt)



# Create a text input for user
st.text_input('**YOU:** ',  key='prompt_input', on_change=submit)

if st.session_state.entered_prompt != "":
    with st.spinner("Generating response..."): # Add spinner here
        # Get user query
        user_query = st.session_state.entered_prompt

        # Append user query to past queries
        st.session_state.past.append(user_query)

        # Generate response
        output = generate_response()

        # Append AI response to generated responses
        st.session_state.generated.append(output)

with st.sidebar:  # Or st.expander("About"):
    st.header("About This Chatbot")
    st.write("This AI Assistant is designed to provide information about **Muhammad Zain** and his services related to **Generative AI** and **Data Science.**  It's powered by Google Gemini and maintained on GitHub.")
    st.markdown("""
    <div style="text-align: left;">
            <!-- GitHub -->
            <a href="https://github.com/muhammadzainrehmani/personal-bot" target="_blank" style="text-decoration: none; margin: 10px;">
                <img src="https://img.icons8.com/ios-glyphs/30/000000/github.png" alt="GitHub"/> View on GitHub
            </a>
    </div>
    """, unsafe_allow_html=True)

    st.title("Follow Me on Social Media")

    # Social media links with icons
    st.markdown("""
    <div style="text-align: left;">
        <!-- LinkedIn -->
        <a href="https://www.linkedin.com/in/muhammad-zain-rehmani" target="_blank" style="text-decoration: none; margin: 10px;">
            <img src="https://img.icons8.com/ios-filled/30/0077b5/linkedin.png" alt="LinkedIn"/> LinkedIn
        </a>
        <br>
        <!-- Personal Website -->
        <a href="https://muhammadzainrehmani.tiiny.site/" target="_blank" style="text-decoration: none; margin: 10px;">
            <img src="https://img.icons8.com/ios-filled/30/4CAF50/domain.png" alt="Website"/> Website
        </a>
        <br>
        <!-- Twitter -->
        <a href="https://twitter.com/m_zain_rehmani" target="_blank" style="text-decoration: none; margin: 10px;">
            <img src="https://img.icons8.com/ios-filled/30/1DA1F2/twitter.png" alt="Twitter"/> Twitter
        </a>
        <br>
        <!-- Instagram -->
        <a href="https://instagram.com/muhammad_zain_rehmani" target="_blank" style="text-decoration: none; margin: 10px;">
            <img src="https://img.icons8.com/ios-filled/30/833AB4/instagram-new.png" alt="Instagram"/> Instagram
        </a>
        <br>
        <!-- Facebook -->
        <a href="https://facebook.com/muhammadzainrehmaniofficial" target="_blank" style="text-decoration: none; margin: 10px;">
            <img src="https://img.icons8.com/ios-filled/30/4267B2/facebook-new.png" alt="Facebook"/> Facebook
        </a>
    </div>
    """, unsafe_allow_html=True)


    
# Display the chat history
if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        # Display AI response
        AI = st.chat_message("ai")
        AI.write(st.session_state["generated"][i], key=str(i))
        # Display user message
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
