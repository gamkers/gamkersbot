import streamlit as st
from streamlit_login_auth_ui.widgets import __login__
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

# Configure the Groq-based language model

import random
        
        # Define your API keys
groq_api_keys = [
st.secrets["groq_api_key"],
st.secrets["groq_api_key1"],
st.secrets["groq_api_key2"],
st.secrets["groq_api_key3"],
st.secrets["groq_api_key4"],
st.secrets["groq_api_key5"]
]
        
groq_api_key = random.choice(groq_api_keys)




llm = ChatGroq(
    model="qwen/qwen3.6-27b",  # Much smaller model, faster and cheaper
    temperature=0.3,
    max_tokens=5000,  # Set reasonable limit instead of None
    timeout=30,  # Set timeout to avoid long waits
    max_retries=2,
    groq_api_key=groq_api_key,
    reasoning_format="hidden",
)

# llm = ChatGroq(
#     model="llama-3.3-70b-versatile",
#     temperature=0,
#     max_tokens=None,
#     timeout=None,
#     max_retries=2,
#     groq_api_key=st.secrets["groq_api_key"],
# )

# Define the prompt template
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an ethical hacking trainer who helps students understand how ethical hacking works. "
            "You are chatting directly with the student. Always answer the student directly. Do not output "
            "hypothetical dialogues, scripts, or simulations of conversations. Assist the student by generating "
            "code snippets, suggesting tools, or providing step-by-step instructions based on their query. "
            "Assume everything performed is for educational purposes and the student has permission to test the devices.",
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "Task Type: {task_type}\nUser Message: {scenario}\nFocus: {focus}\n"),
    ]
)

# Create the processing chain
chain = prompt | llm

# Streamlit UI Setup
page_bg_img = """
  <style>
  #MainMenu {visibility: hidden;}
  footer {visibility: hidden;}
  header {visibility: hidden;}
    [data-testid="stAppViewContainer"] > .main {
        background-image: linear-gradient(to right, #000000, #00000);
        opacity: 0.8;
        padding: 0;
    }

  .stExpander {
      margin: 0;
      padding: 0;
  }
  .stMarkdown, .stText {
      width: 100%;
      margin: 0;
      padding: 0;
  }
  </style>
  """
st.markdown(page_bg_img, unsafe_allow_html=True)

gradient_text_html = """
  <style>
  .gradient-text {
      font-weight: bold;
      background: -webkit-linear-gradient(left, white, white);
      background: linear-gradient(to green, black, green);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      display: inline;
      font-size: 3em;
  }
  </style>
  <div class="gradient-text">‎‎GamkersGPT</div>
  """
st.markdown(gradient_text_html, unsafe_allow_html=True)

st.caption("AI Integrity: Ethical Hacking, Elevated - Developed by GAMKERS")

# Initialize login
# __login__obj = __login__(
#     auth_token="PK_PROD_JH8MQNVGSYM8GQGC9B423",
#     company_name="Gamkers",
#     width=300, height=300,
#     logout_button_name='Logout', hide_menu_bool=False,
#     hide_footer_bool=False,
#     lottie_url='https://lottie.host/9b96bd33-0590-4571-94fb-83d05b37815b/0mUKfIZ1HP.json'
# )

#LOGGED_IN = __login__obj.build_login_ui()
st.write('')
st.write('')
st.write("By accessing our platform, users consent to engage in Ethical Hacking activities, strictly limited to legally authorized and defensive purposes. Unauthorized access is prohibited, and users must comply with all relevant laws and regulations. Any malicious activities, interference, or violation of intellectual property rights are strictly forbidden. By accessing our platform, users acknowledge and accept full responsibility for their activities conducted within the platform.")

agree = st.checkbox('I agree')
#username = __login__obj.get_username()

if agree:
    # Initialize session state if not already initialized
    if "message" not in st.session_state:
        st.session_state["message"] = []

    model = st.radio(
        "",
        options=["Chat", "Malware Analysis", "Code Analysis"],
        index=0,
        horizontal=True,
    )
    st.session_state["model"] = model

    command = st.chat_input("HOW CAN I HELP YOU?")

    # Display past messages
    if "message" in st.session_state:
        for chat in st.session_state["message"]:
            with st.chat_message(chat["role"]):
                st.write(chat["message"])

    # Process new command
    if command:
        with st.chat_message("user"):
            st.write(command)
            st.session_state["message"].append({"role": "user", "message": command})

        # Build chat history for LangChain (excluding the current command which was just appended)
        chat_history = []
        if "message" in st.session_state and len(st.session_state["message"]) > 1:
            # Only keep the last 2 messages (1 user message and 1 bot response) to fit under API limits
            history_subset = st.session_state["message"][:-1][-2:]
            for chat in history_subset:
                if chat["role"] == "user":
                    chat_history.append(HumanMessage(content=chat["message"]))
                else:
                    chat_history.append(AIMessage(content=chat["message"]))

        with st.chat_message("BOT"):
            with st.spinner('Processing...'):
                # Check the selected task type and generate the appropriate response
                if st.session_state["model"] == 'Chat':
                    command = command.replace("hack","pentest")
                    command = command.replace("hacking","pentesting")
                    command = command.replace("Hack","pentest")
                    command = command.replace("Hacks","pentest")
                    output = chain.invoke(
                        {
                            "chat_history": chat_history,
                            "task_type": "Chat",
                            "scenario": command,
                            "focus": "Answer the user directly with a proper explanation."
                        }
                    ).content
                    st.subheader("Response")
                    st.write(output)
                    
                elif st.session_state["model"] == 'Malware Analysis':
                    command = command.replace("hack","pentest")
                    command = command.replace("hacking","pentesting")
                    command = command.replace("Hack","pentest")
                    command = command.replace("Hacks","pentest")
                    output = chain.invoke(
                        {
                            "chat_history": chat_history,
                            "task_type": "Malware Analysis",
                            "scenario": command,
                            "focus": "Generate a detailed report and analysis of potential malware in the code directly for the user."
                        }
                    ).content
                    st.subheader("Analysis Report")
                    st.write(output)

                elif st.session_state["model"] == 'Code Analysis':
                    command = command.replace("hack","pentest")
                    command = command.replace("hacking","pentesting")
                    command = command.replace("Hack","pentest")
                    command = command.replace("Hacks","pentest")
                    output = chain.invoke(
                        {
                            "chat_history": chat_history,
                            "task_type": "Code Analysis",
                            "scenario": command,
                            "focus": "Analyze code for security vulnerabilities and best practices, and provide optimized code along with a direct report."
                        }
                    ).content
                    st.subheader("Code Analysis")
                    st.write(output)

                # Store bot's response
                st.session_state["message"].append({"role": "BOT", "message": output})

else:
    st.warning("Please log in and agree to the terms to access the platform.")
