dict={'assistant_message': {'role': 'assistant', 'content': None, 'function_call': {'name': 'get_doctor', 'arguments': '{\n"typeofDoctor": "Smith"\n}'}}, 'fn_name': 'get_doctor', 'arguments': '{\n"typeofDoctor": "Smith"\n}'}

print(dict['assistant_message']['function_call']['name'])