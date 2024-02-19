from openai import OpenAI
import json
import requests
from datetime import datetime
from dateutil import parser
from datetime import datetime, timedelta
from dateutil import parser


def chat_completion_request(messages, functions=None, function_call=None, model="gpt-3.5-turbo-0613"):
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + "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",
    }
    json_data = {"model": model, "messages": messages}
    if functions is not None:
        json_data.update({"functions": functions})
    if function_call is not None:
        json_data.update({"function_call": function_call})
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
def smallest_difference(given_number, number_list):
    if not number_list:
        return None  # Handle empty list case
    min_difference = float('inf')
    # Initialize with positive infinity to ensure any difference will be smaller
    closest_number = None
    for num in number_list:
        difference = abs(given_number - num)
        ##print(f"difference for {num} is {difference}")
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
def get_doctor(arguments):
    

    # Convert the doctor type to title case to handle case-insensitivity
    doctor_type = json.loads(arguments)['typeofDoctor']
    # check if string contains Dr . or Dr  
    if doctor_type.startswith("Dr "):
        doctor_type=doctor_type[3:]
    else:
        doctor_type=doctor_type
   
    
    #logging.info(list_of_doctors)

    # Check if the provided doctor type exists
    if doctor_type in list(all_doctors.keys()):
        return f"{', '.join(all_doctors[doctor_type])} is available and please confirm the doctor" 
    elif 'Dr. ' + doctor_type.capitalize() in list_of_doctors:
        return f"{doctor_type} is available  what date and time would you like to perfer for appointement"
    else:
        return f"No doctors found for the search you provided: {doctor_type}"
def fix_time_date_appointement(arguments):
    timeslot=json.loads(arguments)['timeslot']
    
    try:

        Date=json.loads(arguments)['Date']
    except KeyError:
        return input("Agent: please enter date of appointement with doctor")
    timeslot=str(timeslot)
    try:
    
            if len(timeslot)==1 or len(timeslot)==2:
                timeslot=f"{timeslot}:00:00"
                #today = None
            if Date=="tommorrow":
                today = datetime.now() + timedelta(days=1)
            elif "-" in Date:
                today = datetime.strptime(Date, "%Y-%m-%d")
                current_year = datetime.now().year
                new_date = datetime(year=current_year, month=today.month, day=today.day)
                print(type(new_date))
                today = new_date
                #today = today.strptime(today, "%Y-%m-%d")
                print(today)
            else:
                today = datetime.now() + timedelta(days=0)
            # Construct the full datetime string for tomorrow with the given time
            datetime_string = f"{today.strftime('%Y-%m-%d')} {timeslot.split()[0]}"
            #print(datetime_string)
            # Parse the full datetime string
            parsed_datetime = datetime.strptime(datetime_string, "%Y-%m-%d %H:%M:%S")
            #print(parsed_datetime)
            # Extract only the time
            parsed_time = parsed_datetime.strftime('%H:%M %p')
            ptime=int(parsed_time[:-2][0:2])
            #print(f"The parsed time is: {ptime}")
            available_time=['10:00 AM - 11:00 AM', '1:00 PM - 4:00 PM']
            total_slots=len(available_time)
            slots_available=[]
            isslotbooked=False
            for available_time_slot in available_time:            
                start_time_str, end_time_str = map(str.strip, available_time_slot.split(' - '))
                start_time = parser.parse(start_time_str)
                start_time=start_time.strftime('%H:%M %p')
                start_time=int(start_time[:-2][0:2])
                slots_available.append(start_time)
                #print(f"start_time is {start_time}")
                end_time = parser.parse(end_time_str)
                end_time=end_time.strftime('%H:%M %p')
                #print(f"end_time is {end_time}")
                end_time=int(end_time[:-2][0:2])
                slots_available.append(end_time)
                #print(f"end_time is {end_time}")
                if start_time <= ptime <= end_time:
                    isslotbooked=True
                    return f" Doctor available at {datetime_string} and call is booked."
                else:
                    #print( slots_available)
                    isslotbooked=False
                    nearestslot=smallest_difference(ptime,slots_available)
                    print(nearestslot)
                    #print(ptime)
                    
                #caluculate the smallest differnce with an list and an given number
            if not(isslotbooked):
                return f"Doctor not available at {datetime_string} and is available at {nearestslot[0]}"


       
    except ValueError:
        return "Invalid input sent"
def fixappointement_doctor(arguments):
    doctorname=json.loads(arguments)['doctorname']
    date=json.loads(arguments)['Date']
    timeslot=json.loads(arguments)['timeslot']
    if doctorname.startswith("Dr. "):
        doctorname=doctorname[3:]
    else:
        doctorname=doctorname

    if doctorname in list(all_doctors.keys()):
        return f"{', '.join(all_doctors[doctorname])} is available and please confirm the doctor" 
    elif 'Dr. ' + doctorname.capitalize() in list_of_doctors:
        dict1=json.loads(arguments)
        del dict1["doctorname"]
        arguments=json.dumps(dict1)
        return f"{doctorname} available.{fix_time_date_appointement(arguments)}"
        
    else:
        return f"No doctors found with name: {doctorname}"

