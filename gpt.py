import openai
import os
openai.api_key = os.getenv('OPENAI_API_KEY')


def send_message(msg):
    c = openai.ChatCompletion.create(
        model = 'gpt-3.5-turbo-0301',
        messages = msg
    )
    msg.append({'role':'assistant', 'content': c.choices[0].message.content})
    cost = c.usage.total_tokens/1000*0.002
    print(f"${'{:.5f}'.format(cost)} - {c.choices[0].message.content}")
    return msg

msg = []
while True:
    question = input("\n> ")
    if question == '\\r':
        print("Chat has been reset.")
        msg = []
        continue
    msg.append({'role': 'user', 'content': question})
    msg = send_message(msg)

