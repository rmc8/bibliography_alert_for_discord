from unittest import TestCase
from unittest.mock import patch, mock_open, MagicMock

import add_path  # noqa: F401
from pkg.yc import YamlConfig


class TestYamlConfig(TestCase):
    @patch("pathlib.Path.exists")
    def test_exists(self, mock_exists):
        mock_exists.return_value = True
        config = YamlConfig("./test.yml")
        self.assertTrue(config.exists())

    @patch("builtins.open", new_callable=mock_open, read_data="version: 2.1\n")
    @patch("pathlib.Path.exists")
    def test_load(self, mock_exists, mock_file):
        mock_exists.return_value = True
        config = YamlConfig("./settings/config.yml")
        data = config.load()
        test_data = {"version": data.get("version")}
        self.assertEqual(test_data, {"version": 2.1})

    @patch("yaml.dump")
    @patch("builtins.open", new_callable=mock_open)
    @patch("pathlib.Path.exists")
    def test_write(self, mock_exists, mock_file, mock_yaml_dump):
        mock_exists.return_value = True
        config = YamlConfig("./test.yml")
        config.write({"key": "value"})
        mock_yaml_dump.assert_called_once()  # Changed here

    @patch("pathlib.Path.exists")
    def test_load_file_not_found(self, mock_exists):
        mock_exists.return_value = False
        config = YamlConfig("./test.yml")
        with self.assertRaises(FileNotFoundError):
            config.load()

    @patch("pathlib.Path.exists")
    def test_write_file_not_found(self, mock_exists):
        mock_exists.return_value = False
        config = YamlConfig("./test.yml")
        with self.assertRaises(FileNotFoundError):
            config.write({"key": "value"})
