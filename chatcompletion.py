from openai import OpenAI
import json
import requests
import finnhub
from datetime import datetime
from dateutil import parser
from datetime import datetime, timedelta
from dateutil import parser
from helper_functions import *
import logging
import time
logging.basicConfig(level=logging.INFO, filename='app.log')

tools = [
{
    "type": "function",
   "function":{
        "name": "get_doctor_by_name",
        "description": """this function must be called only if user specifies  only the doctor name eg: can i have an appointement with doctor smith
        eg: can i have an appointement with Dr smith
        In the above examples smith should be passed as name_of_doctor
        """,
        "parameters": {
            "type": "object",
            "properties": {
                "name_of_doctor": {
                    "type": "string",
                    "description": "This is the  name of doctor  required for patient",
                }
            },
            "required": ["name_of_doctor"],
        },
    }
},
{
    "type": "function",
   "function":{
        "name": "get_doctor_by_department",
        "description": """this function must be called only if user specifies  only the department of doctor 
        eg: can i have an appointement with general physician
        eg: can i have an appointement with Cardiologist
        In the  first example it  should pass Family Medicine as input to  name_of_department
        """,
        "parameters": {
            "type": "object",
            "properties": {
                "name_of_department": {
                    "type": "string",
                    "enum":["Family Medicine","Cardiology","Dermatology","oncology","Pulmonology"],
                    "description": "This is the  department of doctor  required for patient",
                }
            },
            "required": ["name_of_department"],
        },
    }
},
{
   "type": "function",
   "function":{
        "name": "get_time_date_book_appointement",
        "description": """this function is called to fix an appointement with doctor
        it will take two parametrs one is timeslot and other is Date
        timeslot would be like 4 PM,3 AM --etc  and date would be today,tommorrow,feb26th,23-02-2024
        if timeslot is not provided it should set as null
        eg:book a slot for tommorrow
        eg:book an appointement at 4 PM for tommorrow
        eg:book a slot for today at 6 PM
        for the first example timeslot must be null and Date will be tommorrow
        for the second example timeslot will be 16:00 and Date will be tommorrow
        for the third example timeslot will be 18:00 and Date will be today
""",
        "parameters": {
            "type": "object",
            "properties": {
                "timeslot": {
                    "type": "integer",
                    "description": "This is the time  of the appointment  we need to map.",
                },
                "Date":{
                    "type":"string",
                    "description":"This is Date of the appointement we need to map"
                }
                
            },
            "required": ["timeslot","Date"]
            
   }
   }
},

{
   "type": "function",
   "function":{
        "name": "get_time_date_doctor_book_appointement",
        "description": """this function is called to fix an appointement with doctor
        it will take below three parametrs o
        1.timeslot
        2.Date
        3.name_of_doctor
        timeslot would be like 4 PM,3 AM --etc  and date would be today,tommorrow,feb26th,23-02-2024
        name_of_doctor would be Dr. Smith,smith,doctor smith for all the examples with name_of_doctor should be passed as smith.
        if timeslot is not provided it should set as null
        eg:book a slot for tommorrow
        eg:book an appointement with Dr smith at 4 PM for tommorrow
        eg:book a slot  with smith for today at 6 PM
        for the first example timeslot must be null and Date will be tommorrow
        for the second example timeslot will be 16:00 and Date will be tommorrow and name_of_doctor is smith
        for the third example timeslot will be 18:00 and Date will be today and name_of_doctor is smith
""",
        "parameters": {
            "type": "object",
            "properties": {
                "timeslot": {
                    "type": "integer",
                    "description": "This is the time  of the appointment  we need to map.",
                },
                "Date":{
                    "type":"string",
                    "description":"This is Date of the appointement we need to map"
                },
                "name_of_doctor": {
                    "type": "string",
                    "description": "This is the name_of_doctor  we need to map.",
                },
                
            },
            "required": ["timeslot","Date","name_of_doctor"]
            
   }
   }
}

]
user_input = input("Please enter your question here: (if you want to exit then write 'exit' or 'bye'.) ")

def user_input():
    messages = [{"role": "system", "content": "Don't make assumptions about what values to plug into functions. Ask for clarification if a user request is ambiguous."}]
    
    messages.append({"role": "assistant", "content": "Book an appointement with Doctor in Super Clinic and Don't make assumptions about what values to plug into functions. Ask for clarification to user if request dont have parameters to be passed to function."}),

    user_input = input("User: ")

    while user_input.strip().lower() != "exit" and user_input.strip().lower() != "bye":

        # prompt
        
        messages.append({"role": "user", "content": user_input})
        print(messages)
        # calling chat_completion_request to call ChatGPT completion endpoint
        chat_response = chat_completion_request(
            messages, tools=tools
        )
        # fetch response of ChatGPT and call the function
        #print(chat_response.json())
        messages= messages[:-1]
        try:

            if chat_response.json()["choices"][0]["message"] is not None:

                assistant_message = chat_response.json()["choices"][0]["message"]
                logging.info(f'assistant_message-: {chat_response.json()}')
        except KeyError :

                assistant_message = chat_response.json()["error"]["code"]
                logging.info(f'assistant_message-: {assistant_message}')
                print(f'{assistant_message} waiting for  20s')
                time.sleep(21)
                continue


            
        if assistant_message['content']:
            
            print("message from agent without calling function")
            messages.append({"role": "assistant", "content": assistant_message['content']})
            print("Agent : ", assistant_message['content'])
        else:
            print(assistant_message["tool_calls"])
            fn_name = assistant_message["tool_calls"][0]["function"]["name"]
            arguments = assistant_message["tool_calls"][0]["function"]["arguments"]
            #print(globals())
            f1=globals()[fn_name]
            result = f1(arguments)
            logging.info(f'result-: {result}')
            print("Agent : ", result)
            messages.append({"role": "assistant", "content": result})
            #user_input = input("User ")
        user_input = input("User ")
        

user_input()