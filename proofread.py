import json
import os
from translator import is_finished
from translator import load_cookies
from chatgpt_automation import ChatGPT_Client

translated_file_dir = 'translated'
text_file_dir = 'text'

# check if the translated files are duplicated
# 检查翻译后的文件是否有重复的内容
def check_duplication():
    for file in os.listdir(translated_file_dir):
        file_path = translated_file_dir + '\\' + file
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                text = [list(i.values())[0] for i in data]
                if len(text) - len(set(text)) > 5:
                    # print the duplicated elements
                    print(set([x for x in text if text.count(x) > 1]))
                    print(file)
            except:
                pass
    

def proofread_with_gpt3(stepsize=50):
    proofread_session_url = 'https://chat.openai.com/c/38149660-e541-4d00-8190-82024db7599e'
    proofread_cookies = load_cookies(2)

    chatgpt = ChatGPT_Client(proofread_cookies, url=proofread_session_url, answer_waiting_time=1)

    prompt = 'Please compare the following two texts which are in Chinese and Japanese. If they have the same meaning, please answer "1", otherwise answer "0".\n\nChinese:\n'

    for file in os.listdir(translated_file_dir):
        wrong_translation = []
        if is_finished(file):
            with open(f'{translated_file_dir}/{file}', 'r', encoding='utf-8') as f:
                data = json.load(f)
                text = [list(i.values())[0] for i in data]
            with open(f'{text_file_dir}/{file}', 'r', encoding='utf-8') as f:
                raw_text = json.load(f)
                raw_text = [list(i.values())[0] for i in raw_text]
            for i in range(0, len(text), stepsize):
                question = prompt + text[i] + '\n\nJapanese:\n' + raw_text[i]
                answer = chatgpt.interact(question)
                if answer == '0':
                    wrong_translation.append((file, i))
                    print(f'file: {file}, index: {i}')
                    print(question)
                    print(answer)
                    print('-------------------------')
                    print()
                else:
                    print(f'file: {file}, index: {i}')
                    print(question)
                    print(answer)
                    print('-------------------------')
                    print()
        wrongs = "\n".join([str(i) for i in wrong_translation])
        print(f'results:\n{wrongs}')


if __name__ == '__main__':
    proofread_with_gpt3()
    # check_duplication()