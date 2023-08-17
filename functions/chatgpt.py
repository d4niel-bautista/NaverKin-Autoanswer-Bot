import openai
import os

dirname = os.path.dirname(__file__)
token_txt = os.path.join(dirname, 'token.txt')
prompt_txt = os.path.join(dirname, '../prompt.txt')

with open(token_txt, 'r') as f:
    token = f.readline().rstrip()
openai.api_key = token

def get_prompt():
    with open(prompt_txt, 'rb+') as f:
        prompt = f.read().decode('euc-kr')
    return prompt

def generate_response(query):
    prompt = get_prompt()
    messages = [{"role": "system", "content": prompt},
                {"role": "user", "content": query}]
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
    response_message = response["choices"][0]["message"].content
    print(query + '\n---------------\n' + response_message + '\n==================================================\n')
    return response_message
