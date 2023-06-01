# VN-ChatGPT-Translator

一款基于python，使用ChatGPT网页版的视觉小说翻译器，具有以下特点：
- 网页版自动输入文本，**无需api开销**。
- ChatGPT4和ChatGPT3.5均可使用。
- 多账号并发翻译，速度加倍。
- 同一个session内翻译，使得ChatGPT**掌握上下文**，翻译更加精准。
- 使用cookie（推荐）和undetected-chrome登录，方便快捷避免封号。
- 同样支持账号密码登录。
- 自动等待GPT4使用上限，即达到上限后会等待一段时间后自动重启翻译。

## 安装

``` cmd
pip install -r requirements.txt
```

## 项目概述

本项目使用selenium操作ChatGPT网页，使用账号密码或注入cookie以实现登录。登录完成后，会将待翻译的文本以`batch_size`变量指定的句子数量为一批，发送给ChatGPT让其翻译。

## 使用方法

本段将以翻译樱之刻为例子讲解使用方法

### 放置待翻译文本

把待翻译文本放在`./text/`文件夹下，待翻译的对话需要为以下JSON格式：

``` json
[{"静流":"「いらっしゃい」"},
{"？？？":"「……」"},
{"旁白":"一人の男性客が店に入るなり黙ってその場で立ち止まる。"},
{"静流":"「ん？　どうしました？」"},
{"？？？":"「あ、いや、キマイラの店主さんがおかえりだって聞いていたので……」"},
{"静流":"「あれ？　君は、あれかな？　私がいない間のキマイラの常連さん？」"},
{"？？？":"「あ、まぁ、そんな感じですかね」"},
{"旁白":"ずいぶんとすらりとしたイケメンだ。"},
{"旁白":"初対面なのだが、どこかで会った事がある様な。"},
{"静流":"「そうですか。円木ちゃんが店長してた時からの常連さんですか？」"}]
```

你可以参考本项目自带的`./text/01_01.json`中的对话格式。翻译后，生成的文本会储存在`./translated`文件夹下。

### 修改配置文件

以下是`config.py`中的内容

```python
import os


translated_file_dir = 'translated'
text_dir = 'text'

all_text = os.listdir(text_dir)

total_accounts = 1  # 总共账号数量

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
```

你可以按照如下步骤使脚本登录你的ChatGPT账号。

**New Chat** 在ChatGPT网页中新建对话，刷新后将带有编号的浏览器顶部url复制到`urls`变量中。请确保格式为`https://chat.openai.com/c/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`。

**获取cookie** 你可以在edge或chrome浏览器中安装`Cookie-Editor`扩展，并在登录ChatGPT之后将cookie导出（export）为json格式，粘贴进son文件中。之后，你需要将json文件名填写进`cookies_mapping`变量。

**修改提示词（可选）** 把提示词改成更适合你的文本的提示词。

**修改其他配置** 可以根据翻译效果修改。GPT4引擎可以使用15的`batch_size`，即一次输入15句话。GPT3引擎建议数量为10。

### 开始翻译

修改完配置文件后，你可以通过

```
python main.py 1 08:00:00
```

使程序使用账号`1`在系统时间`08:00:00`后开始翻译。开始后，程序会根据账号数量把待翻译的文本分为若干等分，每个账号的翻译任务互不干扰。

### *使用账号密码登录（不推荐）* 

本程序也可以使用账号密码登录，你可以通过修改`Translator`类中`ChatGPT_Client`的构造方式，在其中添加账号密码来实现登录。

### 使用ChatGPT自动校对

`proofread.py`中提供了一些校对翻译是否出现重复、漏句等问题。部分文件翻译完成后，可以运行这个脚本检查是否有错漏。

## 致谢

本项目使用了[ChatGPT-Automation](https://github.com/ugorsahin/ChatGPT_Automation)为基础，并在此之上对原脚本修改使其适合连续翻译长对话。感谢这个脚本的作者。