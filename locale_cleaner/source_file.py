from chardet import detect
from os.path import exists, relpath, basename, splitext
from re import findall, escape, IGNORECASE


class SourceFile:
    """A class representing a source file"""

    def __init__(self, file_path: str, modules: list[str]):
        """Initialize a sourceFile object
        :param file_path: Path to the source file
        :param modules: MODULES to search for
        """
        self.file_path = file_path
        self.modules = modules
        self.modules_constants: dict[str, list[str]] = dict()

    def read(self):
        """Read the source file and find all constants for each module"""

        if not exists(self.file_path):
            raise FileNotFoundError(f"File {self.file_path} not found")
        # Get encoding :
        with open(self.file_path, "rb") as raw_file:
            encoding = detect(raw_file.read())["encoding"]

        # Open file with right encoding :
        with open(self.file_path, "r", encoding=encoding) as file:
            print(f"Reading {self.file_path}...")
            content = file.read()
            for module in self.modules:
                file_name = splitext(basename(relpath(self.file_path)))[0]
                if file_name.lower() == module.lower():
                    regex_pattern = r"([a-zA-Z_]\w*)(?![\[\(])\b"
                else:
                    regex_pattern = (
                        r"\b" + escape(module) + r"\.([a-zA-Z_]\w*)(?![\[\(])\b"
                    )

                self.modules_constants[module] = findall(
                    regex_pattern, content, IGNORECASE
                )

                # DEBUG
                if file_name.lower() == module.lower():
                    print(f"\t -> Results does not be accurate for this file.")
                print(
                    f"\t -> Found {len(self.modules_constants[module])} constants for {module}"
                )

    def get_module_constants(self, module: str) -> list[str]:
        """Return all constants for a module"""
        if module in self.modules_constants:
            return self.modules_constants[module]
        return list()

    def get_modules(self) -> list[str]:
        """Return all modules"""
        return list(self.modules_constants.keys())
