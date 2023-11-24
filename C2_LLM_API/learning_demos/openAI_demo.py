import openai
from importlib.metadata import version
from dotenv import load_dotenv, find_dotenv
import os

print("openai verision: {} ".format(version("openai")))


_ = load_dotenv(find_dotenv())
openai.api_key = os.environ["openai_api_key"]
print("* openai api key loaded")
openai.api_base = "https://smartprompts.net"

name = "聪明的阅读者"
book_summary = """
这是一本讲透阅读方法论的书，全书重点解决“何为读”“如何读”和“读什么”三大难题。
何为读？——你需要知道那些阅读背后的科学原理。这就是全书第一篇介绍的“阅读的系统模型”。
如何读？——你可以师法前沿科学研究与智者实践，这就是全书第二篇介绍的“系统阅读法”，具体包括“文本细读”、“抽样阅读”、“结构阅读”、“主题阅读”，以及“卡片大法”等。
读什么？——你可以读力作、杰作、神作，以及在人类文明历史上的基本书，这就是全书第三篇介绍的“系统选书法”与“通识千书”。
全书文笔优美，金句迭出，同时思想深刻，见解独特。无论你是有阅读刚需的学生，还是想要构建自己知识体系的终身学习者，或是想要培养孩子良好阅读能力和学习能力的家长，这本书都将给你极大的启发和指导。
"""


prompt = (
    "你是最火的小红书博主，现在请你基于书名和书籍简介，为下面这本书写一篇150字的小红书帖子，向粉丝推荐这本书。"
    "请务必使用小红书的语言风格。\n"
    f"书名：{name}"
    f"书籍简介：{book_summary}"
)


def gen(user_input):
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": f"{user_input}",
            }
        ],
        temperature=0.5,
        stream=True,
        max_tokens=300,
    )
    print("* yielding outputs")
    for chunk in response:
        yield chunk.choices[0].delta.content
