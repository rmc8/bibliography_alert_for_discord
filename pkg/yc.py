from pathlib import Path
import yaml


class YamlConfig:
    def __init__(self, file_path: str = "./settings/config.yml"):
        self.file_path = Path(file_path)

    def exists(self) -> bool:
        return self.file_path.exists()

    def load(self) -> dict:
        """
        :return: Return yaml data as dictionary format
        """
        if not self.exists():
            raise FileNotFoundError(f"No such file or directory: '{self.file_path}'")

        with self.file_path.open("r", encoding="utf-8") as yf:
            return yaml.load(yf, Loader=yaml.FullLoader)

    def write(self, data: dict) -> None:
        """
        Export yaml
        :param data: A dictionary of data that will be output in Yaml format
        """
        if not self.exists():
            raise FileNotFoundError(f"No such file or directory: '{self.file_path}'")

        with self.file_path.open("w", encoding="utf-8") as yf:
            yaml.dump(data, yf, default_flow_style=False)
