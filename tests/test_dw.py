import datetime
from unittest.mock import patch, Mock

# escape flake8: F401 (imported but unused)
import add_path  # noqa: F401
from pkg import dw


def test_webhook():
    record = {
        "title": "テストタイトル",
        "author": "テスト著者",
        "isbn": "1234567890",
        "keyword": "テストキーワード",
    }

    url = "https://fake.url"

    expected_payload = {
        "username": "BibliographyAlert",
        "embeds": [
            {
                "title": "新刊の書籍情報",
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

    expected_headers = {"Content-Type": "application/json"}

    mock_response = Mock()
    mock_response.status_code = 203  # DiscordのWebhook APIの成功ステータスコードを反映

    with patch("requests.post", return_value=mock_response) as mock_post:
        dw.webhook(url, record)
        actual_call = mock_post.call_args
        actual_payload = actual_call.kwargs["json"]

        assert actual_payload["username"] == expected_payload["username"]
        assert (
            actual_payload["embeds"][0]["title"]
            == expected_payload["embeds"][0]["title"]
        )
        assert (
            actual_payload["embeds"][0]["fields"]
            == expected_payload["embeds"][0]["fields"]
        )
        # Add more assertions as necessary, excluding the timestamp

    mock_post.assert_called_once_with(
        url, json=actual_payload, headers=expected_headers
    )
