import pyautogui
import time
import speech_recognition as sr
import pyttsx3
from langchain.agents import Tool
from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain_groq import ChatGroq
import requests
from pdfminer.high_level import extract_text
import requests
from io import BytesIO
import fitz  # PyMuPDF

def extract_text_from_pdf_url(pdf_url):
    try:
        # Download the PDF file
        response = requests.get(pdf_url)
        response.raise_for_status()  # Check if the request was successful

        # Open the PDF from the downloaded content
        pdf_document = fitz.open(stream=BytesIO(response.content), filetype="pdf")
        text = ""

        # Iterate through each page
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            text += page.get_text()

        return text 
    except Exception as e:
        print(f"Error: {e}")
        return None

def pdf(s):
    try:
        try:
            from googlesearch import search
        except ImportError:
            print("No module named 'google' found")
        query = f"filetype:pdf {s}"
        for j in search(query, tld="co.in", num=1, stop=5, pause=2):
            if ".pdf" in j:
                k = j.split("/")
                for i in k:
                    if ".pdf" in i:
                        return(j)
                
                
    except Exception as e:
        print(f"Error: {e}")
        print("PDF NOT Found")

def phnumber(my_string):
    print(my_string)
    phonenum = ("91" + my_string.replace(" ", ""))
    url = ("http://apilayer.net/api/validate?access_key=cd3af5f7d1897dc1707c47d05c3759fd&number=" + phonenum)
    resp = requests.get(url)
    details = resp.json()
  
    speak_text("collecting data")
    print('')
    print("Country : " + details['country_name'])
    speak_text("Country : " + details['country_name'])
    print("Location : " + details['location'])
    speak_text("Location : " + details['location'])
    print("Carrier : " + details['carrier'])
    speak_text("Carrier : " + details['carrier'])

def get_voice_input(prompt="Please say something:"):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print(prompt)
        audio = recognizer.listen(source)
        try:
            input_string = recognizer.recognize_google(audio)
            print("You said: " + input_string)
            return input_string
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))

def speak_text(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def schedule_meeting(input_string):
    # Split the string by comma
    elements = input_string.split(',')

    # Assign the elements to variables
    title = elements[0].replace('"',"")
    participants = elements[1].replace('"',"")
    description = elements[2].replace('"',"")
    start_date = elements[3].replace('"',"")
    start_time = elements[4].replace('"',"")
    end_time = elements[5].replace('"',"")

    # Print the variables to verify
    details = f"Title: {title}\nParticipants: {participants}\nDescription: {description}\nStart Date: {start_date}\nStart Time: {start_time}\nEnd Time: {end_time}"
    print(details)
    speak_text(details)

    # Ask for user confirmation
    speak_text("Do you want to proceed with scheduling the meeting? Please say yes or no.")
    confirmation = get_voice_input("Please say yes or no:")
    if confirmation.lower() != 'yes':
        speak_text("Meeting scheduling cancelled.")
        print("Meeting scheduling cancelled.")
        return

    pyautogui.press('win')
    time.sleep(1)
    
    # Type 'Teams' to search for Microsoft Teams
    pyautogui.write('Teams', interval=0.1)
    time.sleep(3)
    
    # Press 'Enter' to open Microsoft Teams
    pyautogui.press('enter')
    time.sleep(3)
    
    # Open Calendar in Teams
    pyautogui.hotkey('ctrl', '5')
    time.sleep(2)  # Wait for the Calendar to open

    # Start a new meeting
    pyautogui.hotkey('alt', 'shift', 'n')
    time.sleep(2)  # Wait for the New Meeting form to open

    # Enter Title
    pyautogui.typewrite(title)
    pyautogui.press('tab')

    # Enter Participants
    pyautogui.typewrite(participants)
    time.sleep(4) 
    pyautogui.press('tab')
    time.sleep(2)
    pyautogui.press('tab')
    time.sleep(2)
    pyautogui.press('tab')
    time.sleep(2)

    # Enter Start Date
    pyautogui.typewrite(start_date)
    pyautogui.press('tab')
    time.sleep(2)
    # Enter Start Time
    pyautogui.typewrite(start_time)
    pyautogui.press('tab')
    time.sleep(2)
    # Enter End Time
    pyautogui.press('tab')

    pyautogui.typewrite(end_time)
    time.sleep(2)
    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.press('tab') 
    pyautogui.typewrite(description)
    pyautogui.press('tab')
    time.sleep(2)
    # pyautogui.hotkey('ctrl', 's')

schedule_meet = Tool(
    name="schedule a meeting in a teams",
    func=schedule_meeting,
    description="Useful for scheduling a meeting in Teams give the title,participants,discription,start_date,start_time,end_time as a list with comma seprated values."
)

 
phone_info = Tool(
    name="information of the phone number",
    func=phnumber,
    description="Useful for fetch a information about a phone number need to parse a phonenumber as argument to the function."
)

pdf_link = Tool(
    name="getting pdf from internet",
    func=pdf,
    description="Useful for fetch a pdf link from internet need to parse the pdf name in the argumnet and it will return a link you need to sumarize it."
)
pdfextract_text_from_pdf_url_tool = Tool(
    name="extract the text from the link",
    func=extract_text_from_pdf_url,
    description="usefull to extract the text from the pdf. need to provide the link to the funtion and it will return the text."
)


prompt_react = hub.pull("hwchase17/react")
print(prompt_react.template)

tools = [schedule_meet,phone_info,pdf_link,pdfextract_text_from_pdf_url_tool]
retrieved_text = ""

# Load ReAct prompt
prompt_react = hub.pull("hwchase17/react")

# Initialize ChatGroq model for language understanding
model = ChatGroq(model_name="llama3-70b-8192", groq_api_key="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", temperature=0)

# Create ReAct agent
react_agent = create_react_agent(model, tools=tools, prompt=prompt_react)
react_agent_executor = AgentExecutor(
    agent=react_agent, tools=tools, verbose=True, handle_parsing_errors=True
)

# Get voice input and schedule the meeting
input_string = input("Please say the meeting details:")
if input_string:
    react_agent_executor.invoke({"input": input_string})
