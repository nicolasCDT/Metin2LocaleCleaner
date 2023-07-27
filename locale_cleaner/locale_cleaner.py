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
        self.locale_files: dict[str, LocaleFile] = {}
        self.source_files: dict[str, SourceFile] = {}
        self.mapping: dict[str, str] = mapping
        self.extensions = extensions or [".py"]
        self.locale_directory = locale_directory
        self.source_directory = source_directory

    def process(self):
        """Process the cleaning"""
        # Read locale files
        for locale_file, source_file in self.mapping.items():
            self.locale_files[source_file] = LocaleFile(
                join(self.locale_directory, locale_file)
            )
            self.locale_files[source_file].read()

        # Read source files
        for root, _, files in walk(self.source_directory):
            for file in files:
                if any(file.endswith(ext) for ext in self.extensions):
                    file_path = join(root, file)
                    self.source_files[file_path] = SourceFile(
                        file_path, list(self.mapping.values())
                    )
                    self.source_files[file_path].read()

        # Find unused keywords
        used_keywords: dict[str, set] = {
            module: set() for module in self.mapping.values()
        }
        for source_file in self.source_files.values():
            for module in self.mapping.values():
                used_keywords[module].update(source_file.get_module_constants(module))

        only_used_keywords: dict[str, list] = {
            module: list() for module in self.mapping.values()
        }
        for module, keywords in used_keywords.items():
            unused_keywords = set(self.locale_files[module].content.keys()) - keywords
            only_used_keywords[module] = [
                keyword
                for keyword in self.locale_files[module].content.keys()
                if keyword not in unused_keywords
            ]
            print(f"Unused keywords count for {module}: {len(unused_keywords)}")

        print("Writing new files...")
        # Writing new locals files
        for locale_file in self.mapping.keys():
            # Detecting encoding :
            with open(join(self.locale_directory, locale_file), "rb") as raw_file:
                encoding = detect(raw_file.read())["encoding"]

            # Writing new file :
            print(f"Writing " + join(self.locale_directory, f"new_{locale_file}") + "...")
            with open(
                join(self.locale_directory, f"new_{locale_file}"),
                "w",
                encoding=encoding,
            ) as file:
                for keyword in only_used_keywords[self.mapping[locale_file]]:
                    file.write(
                        f"{keyword}\t{self.locale_files[self.mapping[locale_file]].content[keyword]}"
                    )
