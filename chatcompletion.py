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
logging.basicConfig(level=logging.INFO, filename='app.log')

        

    

    

functions = [
   
    {
        "name": "get_doctor",
        "description": "It will get the doctor from a clinc.",
        "parameters": {
            "type": "object",
            "properties": {
                "typeofDoctor": {
                    "type": "string",
                    "description": "This is the type of departement to consult or name of doctor  required for patient with issues like Allergy and Immunology,Anesthesiology,Cardiology.",
                }
            },
            "required": ["typeofDoctor"],
        },
    },
    {
        "name": "fix_time_date_appointement",
        "description": "It will check the doctors avalabilty/slots in a clinc by taking time and date as inputs",
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
            
        },
        
        
    },
        {
        "name": "fixappointement_doctor",
        "description": "It will check the doctors avalabilty/slots in a clinc by taking time and date and doctor name as inputs",
        "parameters": {
            "type": "object",
            "properties": {
                "doctorname": {
                    "type": "string",
                    "description": "This is the name of doctor we need to map.",
                },

                "timeslot": {
                    "type": "integer",
                    "description": "This is the time  of the appointment  we need to map.",
                },
                "Date":{
                    "type":"string",
                    "description":"This is Date of the appointement we need to map"
                }
                
            },
            "required": ["timeslot","Date","doctorname"]
            
        },
        
        
    },
    
   
    
    ]
user_input = input("Please enter your question here: (if you want to exit then write 'exit' or 'bye'.) ")

def user_input():
    messages = [{"role": "system", "content": "Don't make assumptions about what values to plug into functions. Ask for clarification if a user request is ambiguous."}]
    
    messages.append({"role": "assistant", "content": "Book an appointement with Doctor in Super Clinic and Don't make assumptions about what values to plug into functions. Ask for clarification to user if request dont have parameters to be passed to function."}),

    user_input = input("User: ")

    while user_input.strip().lower() != "exit" and user_input.strip().lower() != "bye":

        # prompt
        
        messages.append({"role": "user", "content": user_input})
        #print(messages)
        # calling chat_completion_request to call ChatGPT completion endpoint
        chat_response = chat_completion_request(
            messages, functions=functions
        )
        # fetch response of ChatGPT and call the function
        print(chat_response.json())
        assistant_message = chat_response.json()["choices"][0]["message"]
        logging.info(f'assistant_message-: {chat_response.json()}')
        if assistant_message['content']:
            messages.append({"role": "assistant", "content": assistant_message['content']})
            print("Agent : ", assistant_message['content'])
        else:
            
            fn_name = assistant_message["function_call"]["name"]
            arguments = assistant_message["function_call"]["arguments"]
            print(globals())
            f1=globals()[fn_name]
            result = f1(arguments)
            logging.info(f'result-: {result}')
            print("Agent : ", result)
            messages.append({"role": "assistant", "content": result})
            #user_input = input("User ")
        user_input = input("User ")
        

user_input()