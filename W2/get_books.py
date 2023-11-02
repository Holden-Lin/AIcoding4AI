# this code refers to below sources
# https://feizhaojun.com/?p=3813 - usage demo
# https://www.doubanapi.com/ - API deck maintained by a github user

import fire
import requests
from dotenv import load_dotenv, find_dotenv
import os

_ = load_dotenv(find_dotenv())
db_api_key = os.environ["db_api_key"]
print("* db api key loaded")


# 定义一个函数，通过ISBN号从豆瓣API获取书籍摘要
# Type hints explanation:
# Type hints are mainly used for documentation purposes(are not enforced by Python at runtime (they are not type checks))\
# and for use with static analysis tools like mypy, which can analyze your code to find type-related errors without actually running it.
# -> str tells the output data type
def get_book_summary(isbn: str) -> str:
    url = f"https://api.douban.com/v2/book/isbn/{isbn}"

    response = requests.post(
        url,
        data={"apikey": db_api_key},
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.203"
        },
    )
    data = response.json()

    return data.get("summary")


def book_summary(isbn: str = "9787521748536"):
    data = get_book_summary(isbn)
    print(data)


# 如果脚本作为主程序运行，那么获取指定ISBN的书籍摘要并打印
if __name__ == "__main__":
    fire.Fire(book_summary)

"""
需要 pip install requests
python book_summary.py --isbn 9787521748536
此命令将使用提供的ISBN获取书籍摘要
"""
