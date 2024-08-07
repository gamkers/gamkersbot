import streamlit as st
from streamlit_login_auth_ui.widgets import __login__
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

# Configure the Groq-based language model
llm = ChatGroq(
    model="mixtral-8x7b-32768",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    groq_api_key="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",
)

# Define the prompt template
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an assistant that helps ethical hackers by generating code snippets, suggesting tools, or providing step-by-step instructions based on the task and scenario provided.",
        ),
        ("human", "Task Type: {task_type}\nScenario: {scenario}\nFocus: {focus}\n"),
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
    background-image: linear-gradient(to right, #000000, #3c3c50);
    opacity: 0.8;
    padding: 0;
  }
  .stButton > button {
      color: #FFFFFF;
      border-radius: 10%;
      height: 3em;
      width: 6em;
      background: #6528F7;
      border-radius: 16px;
      box-shadow: 0 4px 30px #000000;
      backdrop-filter: blur(12.1px);
      -webkit-backdrop-filter: blur(12.1px);
      border: 1px solid #FF00FF;
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
      background: -webkit-linear-gradient(left, red, orange);
      background: linear-gradient(to right, red, orange);
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
__login__obj = __login__(
    auth_token="PK_PROD_JH8MQNVGSYM8GQGC9B423",
    company_name="Gamkers",
    width=300, height=300,
    logout_button_name='Logout', hide_menu_bool=False,
    hide_footer_bool=False,
    lottie_url='https://lottie.host/9b96bd33-0590-4571-94fb-83d05b37815b/0mUKfIZ1HP.json'
)

LOGGED_IN = __login__obj.build_login_ui()
st.write('')
st.write('')
st.write("By accessing our platform, users consent to engage in Ethical Hacking activities, strictly limited to legally authorized and defensive purposes. Unauthorized access is prohibited, and users must comply with all relevant laws and regulations. Any malicious activities, interference, or violation of intellectual property rights are strictly forbidden. By accessing our platform, users acknowledge and accept full responsibility for their activities conducted within the platform.")

agree = st.checkbox('I agree')
username = __login__obj.get_username()

if LOGGED_IN and agree:
    # Initialize session state if not already initialized
    if "message" not in st.session_state:
        st.session_state["message"] = []

    model = st.radio(
        "",
        options=["Code", "Tools", "Instructions"],
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

        with st.chat_message("BOT"):
            with st.spinner('Processing...'):
                # Check the selected task type and generate the appropriate response
                if st.session_state["model"] == 'Code':
                    output = chain.invoke(
                        {
                            "task_type": "Code",
                            "scenario": command,
                            "focus": "command generation"
                        }
                    ).content
                    st.subheader("Generated Command Snippet:")
                    st.code(output)
                    
                elif st.session_state["model"] == 'Tools':
                    output = chain.invoke(
                        {
                            "task_type": "Tools",
                            "scenario": command,
                            "focus": "tool suggestions"
                        }
                    ).content
                    st.subheader("Suggested Tools:")
                    st.write(output)

                elif st.session_state["model"] == 'Instructions':
                    output = chain.invoke(
                        {
                            "task_type": "Instruction",
                            "scenario": command,
                            "focus": "step-by-step guide"
                        }
                    ).content
                    st.subheader("Instruction Guide:")
                    st.write(output)

                # Store bot's response
                st.session_state["message"].append({"role": "BOT", "message": output})

else:
    st.warning("Please log in and agree to the terms to access the platform.")
