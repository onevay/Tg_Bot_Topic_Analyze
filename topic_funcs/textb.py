from g4f.client import Client

def get_answer(st):
    client = Client()
    content = f'Дай название следующим группам слов, связанных по смыслу, слова уже разбиты по группам. {st}'
    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": content}],
    )
    return response.to_json()['choices'][0]['message']['content']