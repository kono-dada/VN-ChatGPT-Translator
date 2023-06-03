import os


translated_file_dir = 'translated'
text_dir = 'text'

all_text = os.listdir(text_dir)

total_accounts = 1  # 总共账号数量

chrome_version = 113  # Chrome的大版本

# 请在这里放置session的url。
urls = {
    1: 'https://chat.openai.com/c/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx',
}

# 请在这里放置cookies。
cookies_mapping = {1: 'cookie_example.json'}

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