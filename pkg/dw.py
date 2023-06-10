import datetime
import requests

import pytz

japan_tz = pytz.timezone("Asia/Tokyo")


def webhook(url, record):
    now = datetime.datetime.now(japan_tz)
    payload = {
        "username": "BibliographyAlert",
        "embeds": [
            {
                "title": "新刊の書籍情報",
                "timestamp": now.strftime("%Y-%m-%dT%H:%M:%S%z"),
                "footer": {
                    "icon_url": "https://abs.twimg.com/favicons/twitter.ico",
                    "text": "Twitter: @rmc_km",
                },
                "color": 0x0AADB9,
                "author": {
                    "name": "@rmc_km",
                    "url": "https://twitter.com/rmc_km",
                    "icon_url": "https://abs.twimg.com/favicons/twitter.ico",
                },
                "image": {
                    "url": f"http://images.amazon.com/images/P/{record['isbn']}.09_SL110_.jpg"
                },
                "thumbnail": {
                    "url": f"http://images.amazon.com/images/P/{record['isbn']}.09_SL110_.jpg"
                },
                "fields": [
                    {"name": "書籍名", "value": record["title"], "inline": False},
                    {"name": "著者", "value": record["author"], "inline": False},
                    {"name": "Keyword", "value": record["keyword"], "inline": False},
                    {
                        "name": "Link",
                        "value": f"https://www.amazon.co.jp/dp/{record['isbn']}",
                        "inline": False,
                    },
                ],
            }
        ],
    }
    headers = {"Content-Type": "application/json"}
    res = requests.post(url, json=payload, headers=headers)
    print(res)
    print(f"http://images.amazon.com/images/P/{record['isbn']}.09_SL110_.jpg")


# if __name__ == "__main__":
#     webhook(
#         url="https://discord.com/api/webhooks/1116909225529069628/Uu1W0iTWQuCcOUPRxbNYAMoBLCAzhA9YcECfdVeAne_uKNlJOKAqLdJsH2d-NRHXAPjl",
#         record={
#             "title": "初めてのThree.js 第2版",
#             "author": "Jos Dirksen",
#             "isbn": "4802613938",
#             "keyword": "JavaScript",
#         },
#     )
