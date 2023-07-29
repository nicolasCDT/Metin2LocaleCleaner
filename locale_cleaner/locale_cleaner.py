from .locale_file import LocaleFile
from .source_file import SourceFile
from chardet import detect
from os import walk
from os.path import join


class LocaleCleaner:
    """Class to clean unused keywords in locale files"""

    def __init__(
        self,
        mapping: dict[str, str],
        locale_directory="locale",
        source_directory="source",
        extensions=None,
    ):
        """Initialize the class
        :param mapping: Mapping between locale files and python modules
        :param locale_directory: Directory of locale files ("locale" as default)
        :param source_directory: Directory of source files ("source" as default)
        :param extensions: Extensions of source files ([.py] as default)
        """
        self.source_files: dict[str, SourceFile] = {}
        self.mapping: dict[str, str] = mapping
        self.locale_files: dict[str, LocaleFile] = {}
        self.extensions = extensions or [".py"]
        self.locale_directory = locale_directory
        self.source_directory = source_directory

    def read(self):
        # Read locale files
        for locale_file in self.mapping.keys():
            self.locale_files[locale_file] = LocaleFile(
                join(self.locale_directory, locale_file)
            )
            self.locale_files[locale_file].read()

        # Read source files
        for root, _, files in walk(self.source_directory):
            for file in files:
                if any(file.endswith(ext) for ext in self.extensions):
                    file_path = join(root, file)
                    self.source_files[file_path] = SourceFile(
                        file_path, list(self.mapping.values())
                    )
                    self.source_files[file_path].read()

    def process(self):
        """Process the cleaning"""
        self.read()

        # Get used keywords by module
        used_keywords: dict[str, set] = {
            module: set() for module in self.mapping.values()
        }
        for source_file in self.source_files.values():
            for module in source_file.get_modules():
                used_keywords[module].update(source_file.get_module_constants(module))

        # Writing new locals files
        for locale_file in self.mapping.keys():
            file_path = join(self.locale_directory, locale_file)

            print(f"Writing " + file_path + "...")

            # Detecting encoding :
            with open(file_path, "rb") as raw_file:
                encoding = detect(raw_file.read())["encoding"]

            # Write
            with open(file_path, "w", encoding=encoding) as file:
                for key, value in self.locale_files[locale_file].get_content().items():
                    if key in used_keywords[self.mapping[locale_file]]:
                        file.write(f"{key}\t{value}")
        print("Ended ! Enjoy you new cleaned files ! :-)")
