from openai import OpenAI
import json
import requests
import finnhub
import logging
logging.basicConfig(level=logging.INFO, filename='app.log')
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
finnhub_client = finnhub.Client(api_key="Cn28779r01qmg1p4ottgcn28779r01qmg1p4otu0")
def get_current_stock_price(arguments):
    try:
        arguments = json.loads(arguments)['ticker_symbol']
        logging.info(f'arguments to finnhub: {arguments}')

        price_data=finnhub_client.quote(arguments)
        logging.info(f'finnhub_client quote call: {price_data}')
        stock_price = price_data.get('c', None)
        if stock_price == 0:
            return "This company is not listed within USA, please provide another name."
        else:
            return stock_price
    except:
        return "This company is not listed within USA, please provide another name."
def currency_exchange_rate(arguments):
    try:
        from_country_currency = json.loads(arguments)['from_country_currency']
        to_country_currency = json.loads(arguments)['to_country_currency']
        url = f'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={from_country_currency}&to_currency={to_country_currency}&apikey=XG0RD2FKS42D8NM0'
        r = requests.get(url)
        data = r.json()
        logging.info(f'Successful response from {url}: {data}')
        return data['Realtime Currency Exchange Rate']['5. Exchange Rate']
    except requests.RequestException as e:
        return "I am unable to parse this, please try something new.{e}"
functions = [
    {
        "name": "get_current_stock_price",
        "description": "It will get the current stock price of the US company.",
        "parameters": {
            "type": "object",
            "properties": {
                "ticker_symbol": {
                    "type": "string",
                    "description": "This is the symbol of the company.",
                }
            },
            "required": ["ticker_symbol"],
        },
    },
    {
        "name": "currency_exchange_rate",
        "description": "It will get the currency exchange rate between 2 countries.",
        "parameters": {
            "type": "object",
            "properties": {
                "from_country_currency": {
                    "type": "string",
                    "description": "This is the currency of the country whose we need to map.",
                },
                "to_country_currency": {
                    "type": "string",
                    "description": "This is the currency of the country to which we need to map.",
                }
            },
            "required": ["from_country_currency","to_country_currency"],
        },
    }]
user_input = input("Please enter your question here: (if you want to exit then write 'exit' or 'bye'.) ")
while user_input.strip().lower() != "exit" and user_input.strip().lower() != "bye":
    # prompt
    messages = [{"role": "system", "content": "Don't make assumptions about what values to plug into functions. Ask for clarification if a user request is ambiguous."}]
    messages.append({"role": "user", "content": user_input})
    # calling chat_completion_request to call ChatGPT completion endpoint
    chat_response = chat_completion_request(
        messages, functions=functions
    )
    # fetch response of ChatGPT and call the function
    assistant_message = chat_response.json()["choices"][0]["message"]
    logging.info(f'assistant_message-: {chat_response.json()}')
    if assistant_message['content']:
        print("Response is: ", assistant_message['content'])
    else:
        fn_name = assistant_message["function_call"]["name"]
        arguments = assistant_message["function_call"]["arguments"]
        function = locals()[fn_name]
        logging.info(f'locals-: {function}')
        result = function(arguments)
        logging.info(f'result-: {result}')
        print("Response is: ", result)
    user_input = input("Please enter your question here: ")