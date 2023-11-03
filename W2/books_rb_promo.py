"""
DouBanBookUtil 功能介绍如下:
a. _post: 进行POST请求并返回JSON数据。
b. get_book_id_by_name: 根据书名查询书籍ID。
c. get_book_info: 根据书籍ID获取书籍详情。
d. get_book_summary_by_name: 根据书名获取书籍摘要。
e. get_book_summary_by_isbn: 根据ISBN号获取书籍摘要。
"""

import requests, os
from dotenv import load_dotenv, find_dotenv
from datetime import datetime

_ = load_dotenv(find_dotenv())
db_api_key = os.environ["db_api_key"]
print("* db api key loaded")


class BooksRBPromoter:
    def __init__(self, api_key):
        self.db_api_key = api_key

    def parse_date(self, date_str):
        try:
            return datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            try:
                return datetime.strptime(date_str, "%Y-%m")
            except ValueError:
                try:
                    return datetime.strptime(date_str, "%Y")
                except ValueError:
                    return None

    def get_book_info(self, name, *args):
        """
        Retrieves book information based on the book name and optional additional arguments.

        Parameters:
        - book_name (str): The name of the book.
        - *args (str): Optional additional arguments that specify which other information to retrieve.

        Supported args please refer to :
        https://www.doubanapi.com/book.html#%E5%9B%BE%E4%B9%A6%E4%BF%A1%E6%81%AF-book

        You can pass multiple arguments to get multiple pieces of information.

        Returns:
        - dict: A dictionary containing the requested information.

        """

        fields = "id,title,pubdate"
        if args:
            fields += "," + ",".join(args)

        # Append the fields to the API URL
        url = f"https://api.douban.com/v2/book/search?q={name}&fields={fields}"

        response = requests.post(
            url,
            data={"apikey": self.db_api_key},
            headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.203"
            },
        )
        data = response.json()

        if not data.get("books"):
            print("No books found.")
            return None

        matched_book = None
        most_matched_count = 0
        most_recent_date = datetime.min
        books_to_check = 10
        counter = 0

        print("Books returned:")
        for book in data["books"]:
            pubdate_str = book.get("pubdate", "")
            pub_date = self.parse_date(pubdate_str) if pubdate_str else datetime.min
            print(
                f"ID: {book['id']}, Title: {book['title']}, Published Date: {pub_date}"
            )

            if book["title"] == name:
                print("* This is an exact match!")
                if pub_date > most_recent_date:
                    print("* Comparing the pubdate and choose the recent one")
                    most_recent_date = pub_date
                    matched_book = book
            else:
                print("* This is not an exact match")
                match_count = sum(1 for char in name if char in book["title"])
                print(f"* {match_count} words are the matched")

                if match_count > most_matched_count or (
                    match_count == most_matched_count and pub_date > most_recent_date
                ):
                    most_matched_count = match_count
                    matched_book = book
                    most_recent_date = pub_date

            counter += 1
            if counter >= books_to_check:
                print("* Tired after checking 10 books. Let's stop!")
                break

        if matched_book:
            print(
                f"Using this book: ID: {matched_book['id']}, Title: {matched_book['title']}"
            )
            if not args:
                return matched_book["id"]
            else:
                book_info = {"id": book["id"]}
                for arg in args:
                    book_info[arg] = matched_book.get(arg, "Not available")
                return book_info

        else:
            print("No suitable book found.")
            return None


books_rb_promoter = BooksRBPromoter(db_api_key)
book_id = books_rb_promoter.get_book_info("自私的基因", "isbn13", "author")
print(f"The ID returned is: {book_id}")
