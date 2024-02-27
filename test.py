from datetime import datetime, timedelta
from dateutil import parser

input_string = "6"

def smallest_difference(given_number, number_list):
    if not number_list:
        return None  # Handle empty list case
    
    min_difference = float('inf')
    print("min_difference is",min_difference)  # Initialize with positive infinity to ensure any difference will be smaller
    closest_number = None

    for num in number_list:
        difference = abs(given_number - num)
        print(f"difference for {num} is {difference}")
        if difference < min_difference:
            min_difference = difference
            closest_number = num

    return closest_number, min_difference

try:
    # Calculate tomorrow's date
    if len(input_string)==1 or len(input_string)==2:
          input_string=f"{input_string}:00:00"
    today = datetime.now() + timedelta(days=0)
    
    # Construct the full datetime string for tomorrow with the given time
    datetime_string = f"{today.strftime('%Y-%m-%d')} {input_string.split()[0]}"
    print(datetime_string)

    # Parse the full datetime string
    parsed_datetime = datetime.strptime(datetime_string, "%Y-%m-%d %H:%M:%S")

    print(parsed_datetime)






    # Extract only the time
    parsed_time = parsed_datetime.strftime('%H:%M %p')
    ptime=int(parsed_time[:-2][0:2])
    print(f"The parsed time is: {ptime}")

    available_time=['10:00 AM - 11:00 AM', '1:00 PM - 4:00 PM']
    slots_available=[]
    isslotbooked=False
    for available_time_slot in available_time:
                
                start_time_str, end_time_str = map(str.strip, available_time_slot.split(' - '))
                print(start_time_str,end_time_str)
                start_time = parser.parse(start_time_str)
                
                start_time=start_time.strftime('%H:%M %p')
                start_time=int(start_time[:-2][0:2])
                slots_available.append(start_time)
                print(f"start_time is {start_time}")
                end_time = parser.parse(end_time_str)
                end_time=end_time.strftime('%H:%M %p')
                print(f"end_time is {end_time}")
                end_time=int(end_time[:-2][0:2])
                slots_available.append(end_time)
                print(f"end_time is {end_time}")

                if start_time <= ptime <= end_time:
                
                    isslotbooked=True
                    print( f" {parsed_time}.")
                else:
                    isslotbooked=False
                    print( slots_available)
    print(smallest_difference(ptime,slots_available))
#caluculate the smallest differnce with an list and an given number
       
except ValueError:
    print("Invalid input sent")
