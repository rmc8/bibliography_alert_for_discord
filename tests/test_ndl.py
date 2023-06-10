from unittest.mock import patch, Mock
import add_path  # noqa: F401
from pkg.ndl import NationalDietLibrary


@patch("requests.get")
def test_get_bibliography(mock_get):
    mock_response = Mock()
    mock_response.text = "テストタイトル"
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    ndl = NationalDietLibrary()
    params = ["param1"]
    keywords = ["keyword1"]
    bibliography_generator = ndl.get_bibliography(params, keywords)

    bibliography, keyword = next(bibliography_generator)
    assert bibliography == "テストタイトル"
    assert keyword == "keyword1"


@patch("requests.get")
def test_get_isbn(mock_get):
    mock_response = Mock()
    mock_response.text = (
        '<dc:identifier xsi:type="dcndl:ISBN">1234567890</dc:identifier>'
    )
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    ndl = NationalDietLibrary()
    title = "テストタイトル"
    isbn = ndl.get_isbn(title)

    assert isbn == "1234567890"
