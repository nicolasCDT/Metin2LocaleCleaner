# Metin2 Locale File Cleaner

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Description

Metin2 Locale File Cleaner is a Python 3.11 tool designed to clean unused lines from local files in the game Metin2. 
It uses the chardet package (specified in the requirements.txt file) for character encoding detection. 
The tool can be used simply by running the main.py script.

## Usage

1. Clone the repository or download the source code.
2. Install the required dependencies using pip:

```bash
pip install -r requirements.txt
```
3. Configuration
    * Place your locale files in the `locale`directory.
    * Place your source files (root/uiscript/locale) in the `source` directory.
    * Configure the mapping dictionary in the main.py script with the paths to your locale files. For example:
```python
mapping = {
    # "file_name" : "python_file_name"
    "locale_game.txt": "localeInfo",
    "locale_interface.txt": "uiScriptLocale",
}
```
4. Run the main.py script to clean the unused lines from the locale files:
```bash
python main.py
```
You can now use your newly edited locale files located in the locale directory.
## Configuration Options
You can configure the tool using the `LocaleCleaner` class.
* `locale_directory`: Modify the folder for local files (default is `locale`).
* `source_directory`: Modify the folder for source files (default is `source`).
* `extensions`: Modify the extensions to be read by the script (default is `['.py']`).

Refer to the docstring of the `__init__` functions of the `LocaleLCleaner` class for more details on the configuration options.

## Code Formatting
The project has been formatted with [Black](https://github.com/psf/black) for code uniformity.

## License
Metin2 Locale File Cleaner is distributed under the MIT License, which allows you to use, modify, and distribute the tool freely, including for commercial purposes. 
However, you must provide appropriate credit to the [original author](https://github.com/nicolasCDT/).

## Author
Metin2 Locale File Cleaner was created by Nicolas Coudert. 
* Email: [nicolas@coudert.pro](mailto:nicolas@coudert.pro)
* GitHub: [nicolasCDT](https://github.com/nicolasCDT)

Feel free to report any issues or sggest improvements via GitHub issues.

**Happy cleaning!**