import os
import openai
import random
from time import time, sleep


def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()


openai.api_key = open_file('secret.txt')


def save_file(content, filepath):
    with open(filepath, 'w', encoding='utf-8') as outfile:
        outfile.write(content)


def get_next_chunk(filepath, name):
    numbers = filepath.replace('.txt', '').replace(name, '')
    number = int(numbers) + 1
    if number < 10:
        filename = '%s000%s.txt' % (name, number)
    elif number < 100:
        filename = '%s00%s.txt' % (name, number)
    elif number < 1000:
        filename = '%s0%s.txt' % (name, number)
    return open_file('chunks/%s' % filename)

def gpt3_completion(prompt, engine='text-davinci-003', temp=0.7, top_p=1.0,  tokens=300, freq_pen=0.0, pres_pen=0.0, stop=['<<STOP>>']):
    max_retry = 5
    retry = 0
    while True:
        try:
            response = openai.Completion.create(
                engine=engine,
                prompt=prompt,
                temperature=temp,
                max_tokens=tokens,
                top_p=top_p,
                frequency_penalty=freq_pen,
                presence_penalty=pres_pen,
                stop=stop)
            text = response['choices'][0]['text'].strip()
            filename = '%s_gpt3.txt' % time()
            with open('gpt3_logs/%s' % filename, 'w') as outfile:
                outfile.write('PROMPT:\n\n' + prompt + '\n\n==========\n\nRESPONSE:\n\n' + text)
            return text
        except Exception as oops:
            retry += 1
            if retry >= max_retry:
                return "GPT3 error: %s" % oops
            print('Error communicating with OpenAI:', oops)
            sleep(1)


if __name__ == '__main__':
    books = os.listdir('books/')
    for book in books:
        name = book.replace('.txt', '')
        chunks = [i for i in os.listdir('chunks/') if name in i]
        count = 0
        for chunk in chunks:
            count += 1
            prompt = open_file('prompt_questions.txt').replace('<<CONTEXT>>', open_file('chunks/%s' % chunk))
            questions_number = random.randint(1, 5)
            prompt = prompt.replace('<<QUESTIONS_NUMBER>>', f'{questions_number}')
            prompt = prompt.encode(encoding='ASCII', errors='ignore').decode()

            response = gpt3_completion(prompt)
            print(questions_number, name, chunk, response)
            save_file(response, 'questions/%s' % chunk)
            # if count >= 2:
            #     break