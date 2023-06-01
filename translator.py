from chatgpt_automation import ChatGPT_Client
import json
import logging
import time
import os
from configs import *
  

def list_untranslated_files(raw_files:list[str]):
    untranslated_files = [i for i in raw_files if not is_finished(i)]
    return untranslated_files


def is_finished(filename):
    translated_files = os.listdir(translated_file_dir)
    if filename not in translated_files:
        return False
    
    with open(f'{translated_file_dir}/{filename}', 'r', encoding='utf-8') as f:
        try:
            translated_text = json.load(f)
        except:
            return False
    
    with open(f'{text_dir}/{filename}', 'r', encoding='utf-8') as f:
        raw_text = json.load(f)
        return len(translated_text) == len(raw_text)


def load_cookies(account: int):
    cookies_file = cookies_mapping[account]
    mapp = {'lax': 'Lax', 'strict': 'Strict', 'no_restriction': 'None', None: 'None'}
    with open(cookies_file, 'r', encoding='utf-8') as f:
        cookies = json.load(f)
        for i in range(len(cookies)):
            cookies[i]['sameSite'] = mapp[cookies[i]['sameSite']]
    return cookies


class Translator:
    def __init__(self, account: int, start_time:str, headless=True):
        self.account = account
        self.headless = headless
        
        print(f'account {account} will start at {start_time}...')
        # wait until start_time. The start_time is in the format of 'hh:mm:ss'
        while time.strftime('%H:%M:%S', time.localtime()) < start_time:
            time.sleep(60)

        self.chatgpt: ChatGPT_Client = None

        self.time_list = []
        self.start = 0

    
    def create_chatgpt(self):
        if self.chatgpt:
            self.chatgpt.close()

        # load cookies
        cookies = load_cookies(self.account)

        retry_times = 0
        while True:
            try:
                self.chatgpt = ChatGPT_Client(
                    cookies, 
                    url=urls[self.account],
                    use_gpt4=False, 
                    verbose=True,
                    headless=self.headless,
                    answer_waiting_time=answer_waiting_time
                )
            except Exception as e:
                logging.info(e)
                if retry_times < 20:
                    retry_times += 1
                    try:
                        self.chatgpt.close()
                    except:
                        pass
                    logging.info(f'failed to connect to chatgpt, retrying {retry_times} times')
                    time.sleep(300)
                else:
                    logging.info('failed to connect to chatgpt, exiting...')
                    exit()
            else:
                break
  
    
    def start_translate(self, _raw_text=None):
        while True:
            # Any error results in restarting the chatgpt and the translation process
            # 发生的任何错误都会导致重启chatgpt和翻译进程
            try:
                self.create_chatgpt()
                if not _raw_text:
                    raw_text = list_untranslated_files([all_text[i] for i in range(len(all_text)) if i % total_accounts == self.account - 1])
                else:
                    raw_text = _raw_text
                if not raw_text:
                    logging.info('all files have been translated, exiting...')
                    exit()

                for filename in raw_text:
                    if os.path.exists(f'{translated_file_dir}/{filename}'):
                        if is_finished(filename):
                            logging.info(f'{filename} has been translated, skipping...')
                            continue
                        with open(f'{translated_file_dir}/{filename}', 'r', encoding='utf-8') as f:
                            translated_text = f.read()[1:-1]
                            # the number of lines
                            translated_lines = len(translated_text.split('\n')) - 1
                        logging.info(f'continue {filename} from line {translated_lines}')
                    else:
                        translated_lines = 0
                        translated_text = ''
                    logging.info(f'start to translate {filename}')
                    # divide text into batches
                    with open(f'{text_dir}/{filename}', 'r', encoding='utf-8') as f:
                        text = f.read()[1:-1]
                    text = text.split('\n')[translated_lines:]
                    total_lines = len(text)
                    text = ['\n'.join(text[i:i + batch_size]) for i in range(0, len(text), batch_size)]


                    for (i, batch) in enumerate(text):
                        #==============================================
                        if len(self.time_list) >= 8:
                            self.start = self.time_list[-8]
                        self.time_list.append(time.time())
                        # wait until start + 3 hour
                        if time.time() < self.start + 3600:
                            logging.info(f'limit reached, wait until {time.strftime("%H:%M:%S", time.localtime(self.start + 3600))}')
                            while time.time() < self.start + 3600:
                                time.sleep(60)
                            self.create_chatgpt()
                            
                        answer = self.translate_once(batch)
                        if 'error' in answer:
                            logging.info('Error in response')
                            raise Exception('Error in response')
                        if 'cap' in answer:  # reach the capacity. 达到了ChatGPT4上限
                            self.start = time.time()
                            logging.info('cap detected, wait for 1 hours')
                            while time.time() < self.start + 3600:
                                time.sleep(60)
                            raise Exception('cap detected')
                        if 'complete' in answer:  # if the account is a shared account, this might happen. 如果是共享账号，这种情况可能发生
                            logging.info('others are using the account, wait for 5 minutes')
                            time.sleep(60)
                            raise Exception('others are using the account')
                        #==============================================
                        if answer[-1] != ',' and batch != text[-1]:
                            answer += ',\n'
                        else:
                            answer += '\n'
                        translated_text += answer
                        with open(f'{translated_file_dir}/{filename}', 'w', encoding='utf-8') as f:
                            f.write(f'[{translated_text}]')
                        logging.info(f'{(i+1)*batch_size} / {total_lines} finished in {filename}')
            except Exception as e:
                # if keyboard interrupt, exit
                if e == KeyboardInterrupt:
                    break
                logging.info(e)

    def translate_once(self, batch:str):
        message = prompt + batch
        answer = self.chatgpt.interact(message)
        
        return answer
 

if __name__ == '__main__':
    print('\n'.join(list_untranslated_files(os.listdir(text_dir))))