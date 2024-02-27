import os
import time
import logging
from datetime import datetime
import time
import openai

from dotenv import load_dotenv # The dotenv library's load_dotenv function reads a .env file to load environment variables into the process environment. This is a common method to handle configuration settings securely.

# Load env variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.DEBUG, filename='app.log')

from openai import OpenAI
client = OpenAI()

class ThreadManager:
    def __init__(self, client):
        self.client = client
        self.threads = {}  # In-memory dictionary to store threads

    def get_or_create_thread(self, thread_id=None):
        if thread_id and thread_id in self.threads:
            print(f"Retrieving existing thread with ID: {thread_id}")
            return self.threads[thread_id]
        else:
            new_thread = self.client.beta.threads.create()
            thread_id = new_thread.id  # Assuming the thread object has an 'id' attribute
            self.threads[thread_id] = new_thread
            print(f"Created new thread with ID: {thread_id}")
            return new_thread
        
def wait_for_run_completion(client, thread_id, run_id, sleep_interval=5):
    """
    Waits for a run to complete and prints the elapsed time.:param client: The OpenAI client object.
    :param thread_id: The ID of the thread.
    :param run_id: The ID of the run.
    :param sleep_interval: Time in seconds to wait between checks.
    """
    while True:
        try:
            run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
            if run.completed_at:
                elapsed_time = run.completed_at - run.created_at
                formatted_elapsed_time = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
                logging.info(f"Run completed in {formatted_elapsed_time}")
                break
        except Exception as e:
            logging.error(f"An error occurred while retrieving the run: {e}")
            break
        logging.info("Waiting for run to complete...")
        time.sleep(sleep_interval)

"""file = client.files.create(
  file=open("factorial.py", "rb"),
  purpose='assistants'
)
"""
"""
assistant = client.beta.assistants.create(
  name = "Coding Assistant v1.0.0",
  instructions = "You are a personal coding assistant. When asked a coding question, write and run code to answer the question.",
  model = "gpt-3.5-turbo-1106",
  tools = [{"type": "code_interpreter"}],
  file_ids = [file.id]
)
"""
assistant="asst_iyEmDwx3QzeKVAQS96egt2ws"
"""client.beta.assistants.files.list(assistant.id)
"""
# Example usage

thread_manager = ThreadManager(client)

# To get or create a thread
thread = thread_manager.get_or_create_thread()
#thread = client.beta.threads.create()
message = "What's wrong with my implementation of factorial function?"

message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content=message
)

run = client.beta.threads.runs.create(
    thread_id = thread.id,
    assistant_id = assistant,
    instructions = "Please address the user as Gunnar. The user has a premium account."
)

wait_for_run_completion(client, thread.id, run.id)
messages = client.beta.threads.messages.list(
    thread_id=thread.id
    )
last_message = messages.data[0]

text = last_message.content[0].text.value
print('first message',text)

thread = thread_manager.get_or_create_thread()
message = "Yes, please!"

message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content=message
)

run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id,
)

wait_for_run_completion(client, thread.id, run.id)
messages = client.beta.threads.messages.list(
    thread_id=thread.id
    )
last_message = messages.data[0]

text = last_message.content[0].text.value
print('second message',text)

"""
message = "Yes, please!"

message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content=message
)

run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant,
)


messages = client.beta.threads.messages.list(
    thread_id=thread.id
    )

last_message = messages.data[0]

text = last_message.content[0].text.value
print('second message',text)
wait_for_run_completion(client, thread.id, assistant)



run_steps = client.beta.threads.runs.steps.list(
  thread_id=thread.id,
  run_id=run.id
)

"""