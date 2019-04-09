# Mechanics-log-parser

Parse the martionlabs mechanics log into a Discord-friendly table

The arcdps mechanics plugin records a log of all mechanics happening
throughout a raid run. This script loads it, looks for the information related
to a given boss and puts it in a table made from Unicode characters, so it can
be pasted on Discord using the code (```code```) environment. If the pyperclip
Python module is available, the code (including the ```) will directly be
copied into the clipboard.


How to use this script
There are three ways of loading a log:
♦ in the Windows explorer, drop the log on the python script
♦ launch the script, enter the log name
♦ launch the script and simply hit return. The latest log will be parsed
Note: as of 2019-04-09, the plugin creates the log file only after the gw2
client is closed. This can be overriden by opening the mechanics chart window
(Alt+Shift+N) and clicking "export"

The log includes mechanics for all the bosses encountered while the gw2 client
was running. As a consequence, the created table will encompass all the
attempts on a given boss. The "pull" column should reflect that number of
attempts. It should tell if players only came for some attempts.

It also records a single "was downed" number for all of the fights, so
if different bosses are fought, there is no way of telling how many times a
player was downed on a specific encounter. It should be possible to circumvent
this by hitting "export" and "reset" between different bosses, so each of them
has its own log.


Requirements/dependencies
♦ Unicode_table.py: this script is imported and used to draw the table around
the data
♦ pyperclip: automatically copies the table in the clipboard. Not required.


The mechanics log plugin can be found at
http://martionlabs.com/arcdps-mechanics-log-plugin/
