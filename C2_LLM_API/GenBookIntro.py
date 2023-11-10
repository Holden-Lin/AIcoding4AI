import fire
import zhipuai
from dotenv import load_dotenv, find_dotenv
import os
from .GetBookInfo import GetBookInfo


class BookPromoter:
    def __init__(self):
        _ = load_dotenv(find_dotenv())
        self.zp_api_key = os.environ["zp_api_key"]
        self.db_api_key = os.environ["db_api_key"]
        print("* api keys loaded")

    def generate_intro(self, name):
        get_book_info = GetBookInfo(self.db_api_key)
        book_info = get_book_info.get_book_info(name, "summary")

        if book_info is None or "summary" not in book_info:
            print(f"there is no book info for {name}")
            return

        book_summary = book_info["summary"]
        prompt = (
            "你是最火的小红书博主，现在请你基于书名和书籍简介，为下面这本书写一篇150字的小红书帖子，向粉丝推荐这本书。"
            "请务必使用小红书的语言风格。\n"
            f"书名：{name}"
            f"书籍简介：{book_summary}"
        )

        zhipuai.api_key = self.zp_api_key

        response = zhipuai.model_api.sse_invoke(
            model="chatglm_turbo",
            prompt=[
                {"role": "user", "content": f"{prompt}"},
            ],
            # 值越大，会使输出更随机
            temperature=0.8,
            # incremental=True,
        )

        print("* yielding stream ouput")
        for event in response.events():
            if event.event == "add":
                yield event.data
            elif event.event in ["error", "interrupted"]:
                yield f"\nError or Interrupted: {event.data}"
                break
            elif event.event == "finish":
                print("* stream output finished")
                break


def main():
    fire.Fire(BookPromoter)


if __name__ == "__main__":
    main()
