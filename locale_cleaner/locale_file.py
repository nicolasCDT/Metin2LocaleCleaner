from chardet import detect
from os.path import exists


class LocaleFile:
    """Represents a locale file, with its path and its keywords"""

    def __init__(self, file_path: str):
        """Initialize a LocaleFile object
        :param file_path: Path to the locale file
        """
        self.file_path: str = file_path
        self.content: dict[str, str] = dict()

    def read(self):
        """Read the locale file and get all keywords"""
        if not exists(self.file_path):
            raise FileNotFoundError(f"File {self.file_path} not found")

        # Get encoding :
        with open(self.file_path, "rb") as raw_file:
            encoding = detect(raw_file.read())["encoding"]

        # Open file with right encoding :
        with open(self.file_path, "r", encoding=encoding) as file:
            print(f"Reading {self.file_path}...")
            for line in file.readlines():
                if keys := line.split("\t"):
                    if keys[0] in self.content.keys():
                        print(f"\t -> WARNING: Duplicate keyword {keys[0]}")
                    self.content[keys[0]] = "\t".join(keys[1:])

        if not len(self.content.keys()):
            print(f"\t WARNING: No keywords found")

    def get_content(self) -> dict[str, str]:
        """Return the content of the locale file
        :return: Content of the locale file
        """
        return self.content
