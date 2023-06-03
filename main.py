from translator import Translator
import sys
import os


# get an argument from the console
# the argument is the account number

if __name__ == '__main__':
    if not os.path.exists('translated'):
        os.mkdir('translated')
    account = int(sys.argv[1])
    start_time = sys.argv[2]
    translator = Translator(account, start_time)  # 可以添加headless=False来显示浏览器，方便调试
    translator.start_translate()
    translator.chatgpt.close()