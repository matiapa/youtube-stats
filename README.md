# YouTube Stats

This is a simple program for generating useful statistics about your YouTube watch history.

## How to use

1.  Go to https://takeout.google.com/settings/takeout.
2.  Choose only YouTube on the list of products to export.
3.  Choose only watch history on the list of data to export.
4.  Choose JSON as the export format of the watch history.
5.  Choose ZIP as export format and wait for the export to finish.
6.  Extract the watch history file, it's extension is .json.
7.  Rename it as "history.json" and put it on the "in/" folder.
8.  Run with "python main.py", data will be generated on the "out/" folder.