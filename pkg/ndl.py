import re
import html
import itertools
from typing import Optional, Tuple, Iterator
from datetime import date, timedelta

import requests


class NationalDietLibrary:
    """Wrapper for the National Diet Library's OpenSearch and SRU APIs."""

    BASE_SRU_URL = "https://iss.ndl.go.jp/api/sru?operation=searchRetrieve&query={param}=%22{keyword}%22%20AND%20from=%22{date:%Y-%m}"
    BASE_OS_URL = "https://iss.ndl.go.jp/api/opensearch?title={title}"

    def __init__(self, offset: int = 30):
        """Initializes the NationalDietLibrary with a search date offset."""
        self.dt = date.today() - timedelta(days=offset)

    def get_bibliography(
        self, params: list, keywords: list
    ) -> Iterator[Tuple[str, str]]:
        """Yields bibliographic information and the keyword used to find it."""
        for param, keyword in itertools.product(params, keywords):
            url = self.BASE_SRU_URL.format(param=param, keyword=keyword, date=self.dt)
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception if the request was unsuccessful
            yield html.unescape(response.text), keyword

    def get_isbn(self, title: str) -> Optional[str]:
        """Returns the ISBN associated with the given title, if it exists."""
        url = self.BASE_OS_URL.format(title=title)
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception if the request was unsuccessful
        text = html.unescape(response.text)
        match = re.search(
            r'(?<=<dc:identifier xsi:type="dcndl:ISBN">)\d+(?=</dc:identifier>)', text
        )
        return match.group() if match else None
