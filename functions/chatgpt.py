import openai

with open('token.txt', 'r') as f:
    token = f.readline().rstrip()
openai.api_key = token

def get_prompt():
    with open('../prompt.txt', 'r') as f:
        prompt = f.read()
    return prompt

def generate_response(query):
    prompt = get_prompt()
    messages = [{"role": "system", "content": prompt},
                {"role": "user", "content": query}]
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
    response_message = response["choices"][0]["message"].content
    print(query, '\n', response_message)
    return response_message

x = generate_response("this is a test")
