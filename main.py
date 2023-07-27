#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Description: Read your locales files and your source code to remove all unused local variables.
Author: nicolasCDT (mailto:nicolas@coudert.pro - https://www.github.com/nicolasCDT)
Version: 1.0
Date: Created on (07/27/2023)

Disclaimer: This script is provided as is, without any warranty. Use it at your own risk.
"""

from locale_cleaner.locale_cleaner import LocaleCleaner

mapping_tables = {
	# "file_name" : "python_file_name"
	"locale_game.txt": "localeInfo",
	"locale_interface.txt": "uiScriptLocale",
}


def main():
	""" Main entry point of the program """
	locale_cleaner = LocaleCleaner(mapping_tables)
	locale_cleaner.process()


if __name__ == '__main__':
	main()
