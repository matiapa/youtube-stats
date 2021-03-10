# YouTube Stats

This is a simple program for generating useful statistics about your YouTube watch history.

## How to use

0.  Download latest version of Python.
1.  Run "pip install -r .\requirements.txt".
2.  Go to https://takeout.google.com/settings/takeout.
3.  Choose only YouTube on the list of products to export.
4.  Choose only watch history on the list of data to export.
5.  Choose JSON as the export format of the watch history.
6.  Choose ZIP as export format and wait for the export to finish.
7.  Extract the watch history file, it's extension is .json.
8.  Rename it as "history.json" and put it on the "in/" folder.
9.  Run with "python main.py", data will be generated on the "out/" folder.