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

    def __contains__(self, keyword: str) -> bool:
        """Check if a keyword is in the locale file
        :param keyword: Keyword to check
        :return: If the keyword is in the locale file
        """
        return keyword in self.content.keys()

    def __str__(self) -> str:
        """Return a string representation of the LocaleFile object"""
        return f"LocaleFile({self.file_path})"

    def __repr__(self) -> str:
        """Return a representation of the LocaleFile object"""
        return self.__str__()
