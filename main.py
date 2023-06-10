import time
from typing import Optional, List

from pandas import DataFrame
from bs4 import BeautifulSoup, Tag

from pkg.db import SQLite
from pkg.yc import YamlConfig
from pkg.ndl import NationalDietLibrary
from pkg.dw import webhook


def _check_digit(cd_sum: int) -> str:
    cd_num: int = 11 - (cd_sum % 11)
    if cd_num == 10:
        return "X"
    elif cd_num == 11:
        return "0"
    return str(cd_num)


def isbn13to10(isbn13: str) -> str:
    isbn_base = isbn13[3:12]
    cd_sum: int = sum([int(n) * (10 - i) for i, n in enumerate(isbn_base)])
    cd: str = _check_digit(cd_sum)
    return f"{isbn_base}{cd}"


def get_and_convert_isbn(api, title: str) -> Optional[str]:
    time.sleep(1)
    isbn: Optional[str] = api.get_isbn(title=title)
    if isbn is not None:
        isbn = isbn13to10(isbn)
    return isbn


def parse_bibliography_record(html_record) -> Optional[dict]:
    raw_title = (
        None
        if html_record.find("dc:title") is None
        else html_record.find("dc:title").text
    )
    if raw_title is None:
        return None
    title = raw_title.replace("　", " ")
    author = (
        None
        if html_record.find("dc:creator") is None
        else html_record.find("dc:creator").text
    )
    return {"title": title, "author": author}


def create_record(api, title_list: list, html_record: Tag) -> Optional[dict]:
    record = parse_bibliography_record(html_record)
    if record is None or record["title"] in title_list:
        return None
    isbn: Optional[str] = get_and_convert_isbn(api, record["title"])
    if isbn is None:
        return None
    record["isbn"] = isbn
    return record


def parse_bibliography(html: str) -> List[Tag]:
    bs = BeautifulSoup(html, "lxml-xml")
    return bs.find_all("record")


def get_bibliography_records(
    api, title_list: list, params: list, keywords: list
) -> List[dict]:
    records = []
    for html, keyword in api.get_bibliography(params=params, keywords=keywords):
        for html_record in parse_bibliography(html):
            record = create_record(api, title_list, html_record)
            if record is not None:
                record["keyword"] = keyword
                records.append(record)
        time.sleep(1)
    return records


def get_bibliography_df(title_list: list, params: list, keywords: list) -> List[dict]:
    api = NationalDietLibrary(offset=90)
    records = get_bibliography_records(api, title_list, params, keywords)
    return records


def load_settings() -> dict:
    yc = YamlConfig(file_path="./settings/config.yml")
    yml: dict = yc.load()
    return yml["settings"]


def send_discord_alert(webhook_url: str, records: List[dict]) -> None:
    for record in records:
        webhook(url=webhook_url, record=record)


def main():
    settings = load_settings()
    api_settings: dict = settings["api"]
    discord_settings: dict = settings["discord"]
    bibliography_db = SQLite("./db/bibliography.db")

    try:
        db_df: DataFrame = bibliography_db.get_table()
        records: List[dict] = get_bibliography_df(
            title_list=list(db_df.title),
            params=api_settings["params"],
            keywords=api_settings["keywords"],
        )
        if not records:
            return

        webhook_url = discord_settings["webhook_url"]
        send_discord_alert(webhook_url, records)
    finally:
        bibliography_db.close()


if __name__ == "__main__":
    main()
