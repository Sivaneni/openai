from openai import OpenAI
import json
import requests
from datetime import datetime
from dateutil import parser
from datetime import datetime, timedelta
from dateutil import parser
import os
from dotenv import load_dotenv
load_dotenv()
    """
    A function for making a chat completion request to the OpenAI API.

    :param messages: List of messages to be completed.
    :param tools: (optional) List of tools to be used for completion.
    :param tool_choice: (optional) The specific tool to be used for completion.
    :param model: (optional) The model to be used for completion.
    :return: The response object from the API request.
    """
def chat_completion_request(messages, tools=None, tool_choice=None, model="gpt-3.5-turbo-0613"):
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + os.getenv("OPENAIAPI_KEY"),
    }
    print(headers)
    json_data = {"model": model, "messages": messages}
    if tools is not None:
        json_data.update({"tools": tools})
    if tool_choice is not None:
        json_data.update({"tool_choice": tool_choice})
        json_data.update({"temperature": 1.0})
    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=json_data,
        )
        return response
    except Exception as e:
        print("Unable to generate ChatCompletion response")
        print(f"Exception: {e}")
        return e
    """
    Find the number in the given list that is closest to the given number and return both the closest number and the minimum difference.
    Parameters:
    - given_number: a number for which the closest number needs to be found
    - number_list: a list of numbers among which the closest number needs to be found
    Returns:
    - closest_number: the number in the list that is closest to the given number
    - min_difference: the minimum difference between the given number and the closest number
    """
def smallest_difference(given_number, number_list):
    if not number_list:
        return None  # Handle empty list case
    min_difference = float('inf')
    closest_number = None
    for num in number_list:
        difference = abs(given_number - num)
        if difference < min_difference:
            min_difference = difference
            closest_number = num
    return closest_number, min_difference


all_doctors = {
        'Family Medicine': ['Dr. Smith', 'Dr. Johnson', 'Dr. Brown'],
        'Cardiology': ['Dr. Davis', 'Dr. Wilson', 'Dr. Taylor'],
        'Dermatology': ['Dr. Anderson', 'Dr. White', 'Dr. Harris'],
        'oncology':['Dr. Raghu'],
        'Pulmonology':['Dr. Pavan']
        # Add more doctor types and their respective lists
    }
list_of_doctors=[doctor for sublist in all_doctors.values() for doctor in sublist]

    """
    This function retrieves a doctor's information by their name and returns a message regarding their availability for appointments. 
    """
def get_doctor_by_name(arguments):
    
    print(f"function called get_doctor_by_name {arguments}")
    doctor_type = json.loads(arguments)['name_of_doctor']
    if doctor_type.startswith("Dr "):
        doctor_type=doctor_type[3:]
    else:
        doctor_type=doctor_type
    if 'Dr. ' + doctor_type.capitalize() in list_of_doctors:
        return f"{doctor_type} is available  what date and time would you like to perfer for appointement"
    else:
        return f"No doctors found for the search you provided: {doctor_type}"
	"""
	Function to retrieve doctors by department and return their availability or a message if no doctors are found.
	@param arguments: JSON string containing the name of the department
	@return: String indicating the availability of doctors or a message if no doctors are found
	"""
def get_doctor_by_department(arguments):

    print(f"function called get_doctor_by_department {arguments}")
    department = json.loads(arguments)['name_of_department']
    if department in list(all_doctors.keys()):
        return f"{', '.join(all_doctors[department])} is available and please confirm the doctor" 
    else:
        return f"No doctors found for the search you provided: {department}"
            """
    A function to book an appointment with a doctor. It checks for the availability of the doctor at the given timeslot and date, and returns a message indicating if the appointment is booked or if the doctor is not available at that time.
    """
def get_time_date_book_appointement(arguments):
    print(f"function called get_time_date_book_appointement {arguments}")
    keys_to_check=["timeslot","Date"]
    for key in keys_to_check:
        try:
            print(key)
            value=json.loads(arguments)[key]
            print(value)
            if value is None:
                return f"please enter {key} for appointement with doctor"
        except KeyError:
            return f"Agent: please enter {key} for appointement with doctor"
    timeslot=json.loads(arguments)['timeslot']
    Date=json.loads(arguments)['Date']
    timeslot=str(timeslot)
   try:
       if len(timeslot) == 1 or len(timeslot) == 2:
           timeslot = f"{timeslot}:00:00"
   
       if Date == "tomorrow":
           today = datetime.now() + timedelta(days=1)
       elif "-" in Date:
           today = datetime.strptime(Date, "%Y-%m-%d")
           current_year = datetime.now().year
           new_date = datetime(year=current_year, month=today.month, day=today.day)
           today = new_date
       else:
           today = datetime.now() + timedelta(days=0)
   
       datetime_string = f"{today.strftime('%Y-%m-%d')} {timeslot.split()[0]}"
       parsed_datetime = datetime.strptime(datetime_string, "%Y-%m-%d %H:%M:%S")
       parsed_time = parsed_datetime.strftime('%H:%M %p')
       ptime = int(parsed_time[:-2][0:2])
   
       available_time = ['10:00 AM - 11:00 AM', '1:00 PM - 4:00 PM']
       slots_available = []
       isslotbooked = False
   
       for available_time_slot in available_time:
           start_time_str, end_time_str = map(str.strip, available_time_slot.split(' - '))
           start_time = datetime.strptime(start_time_str, '%I:%M %p').hour
           end_time = datetime.strptime(end_time_str, '%I:%M %p').hour
           slots_available.extend([start_time, end_time])
   
           if start_time <= ptime <= end_time:
               isslotbooked = True
               return f"Doctor available at {datetime_string} and call is booked."
           else:
               isslotbooked = False
               nearestslot = smallest_difference(ptime, slots_available)
   
       if not isslotbooked:
           return f"Doctor not available at {datetime_string} and is available at {nearestslot[0]}"
   except ValueError:
       return "Invalid input sent"
    """
    This function processes the input arguments to book an appointment with a doctor. It extracts the doctor's name, date, and time slot from the input JSON, checks the availability of the doctor, and returns a confirmation message or an error message if the doctor is not found.
    """
def get_time_date_doctor_book_appointement(arguments):
   data = json.loads(arguments)
   doctorname = data['name_of_doctor']
   date = data['Date']
   timeslot = data['timeslot']
   
   if doctorname.startswith("Dr. "):
       doctorname = doctorname[3:]
   
   if doctorname in all_doctors:
       return f"{', '.join(all_doctors[doctorname])} is available and please confirm the doctor"
   elif 'Dr. ' + doctorname.capitalize() in set_of_doctors:
       del data["name_of_doctor"]
       arguments = json.dumps(data)
       return f"{doctorname} available.{get_time_date_book_appointment(arguments)}"
   else:
       return f"No doctors found with name: {doctorname}"