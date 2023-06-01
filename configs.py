import os


translated_file_dir = 'translated'
text_dir = 'text'

all_text = os.listdir(text_dir)

total_accounts = 4

# put the session urls here
# 请在这里放置session的url。如果你不知道这是什么，请参考README.md
urls = {
    1: 'https://chat.openai.com/c/cba96978-4255-4713-82cd-f2cced52a4da',
    2: 'https://chat.openai.com/c/425d1705-7e79-46cf-b1e7-29f6ce59fe1f',
    3: 'https://chat.openai.com/c/f893aac8-d7fb-4267-ba22-709a5efce5c1',
    4: 'https://chat.openai.com/c/b6720ac2-400e-46b4-8c32-5cd2acf693dd'
}

# put the cookies here
# 请在这里放置cookies。如果你不知道这是什么，请参考README.md
cookies_mapping = {1: 'cookie1.json', 2: 'cookie2.json', 3: 'cookie3.json', 4: 'cookie4.json'}

prompt = 'please translate the following galgame conversations from Japanese to Chinese. ' + \
        'Please preserve escape characters like \\r\\n or \\" and strictly keep the JSON format of the provided content. ' + \
        'Please directly give the translated content only. ' +\
        'Here are the conversations:\n'

# the time to wait for the answer from the chatbot. If the bot waits too short, error may occur.
# 等待聊天机器人回答的时间。如果等待时间太短，可能会出现错误。
answer_waiting_time = 10

# the maximum number of lines to input to ChatGPT each time
# 每次输入ChatGPT的最大行数
batch_size = 15