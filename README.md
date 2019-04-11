# Mechanics-log-parser

Parse the [Martion Laboratories mechanics log](http://martionlabs.com/arcdps-mechanics-log-plugin/) into a Discord-friendly table


### Description:

The arcdps mechanics plugin records a log of all mechanics happening
throughout a raid run. This script loads it, looks for the information related
to a given boss and puts it in a table made from Unicode characters, so it can
be pasted on Discord using the ```code``` (\`\`\`code\`\`\`) environment. If the pyperclip
Python module is available, the code (including the \`\`\`) will directly be
copied into the clipboard.

To quote Martion Labs: "This plugin is not intended to breed toxicity, but
instead help show players mechanical areas where the players can improve. This
is in the same way that arcdps shows how dps/boons could be improved."
The purpose of this script is to help with this, by turning that information
into a table that can be easily read by everyone.


### How to use this script:

There are three ways of loading a log:
- in the Windows explorer, drop the log on the python script
- launch the script, enter the log name
- launch the script and simply hit return. The latest log will be parsed

On first run, the script will ask for the gw2 documents directory. The
directory will be saved in mechanics_log_settings.ini for subsequent runs.

If the log contains the data for several bosses, the script will ask which
boss fights should be processed. It is possible to answer with more than one
fight, using commas (1, 2, 4 for example). The bosses will be processed one
after the other.
If the win32api module is not installed, the script will move on to the next
boss after return has been used.
If it is installed, the script will move on after a specific key (set in
mechanics_log_settings.ini, using virtual key codes from
https://docs.microsoft.com/en-us/windows/desktop/inputdev/virtual-key-codes )
has been pressed and released. The default value for this key is "V", so that
pasting the log in Discord using ctrl+V automatically triggers the next log
processing.


### Remarks:

- As of 2019-04-09, the plugin creates the log file only after the gw2 client is
closed. This can be overriden by opening the mechanics chart window
(Alt+Shift+N) and clicking "export".

- The log includes mechanics for all the bosses encountered while the gw2 client
was running. As a consequence, the created table will encompass all the
attempts on a given boss. The "pull" column should reflect that number of
attempts. It should tell if players only came for some attempts.

- It also records a single "was downed" number for all of the fights, so if
different bosses are fought, there is no way of telling how many times a
player was downed on a specific encounter.

- It seems that hitting "export" and "reset" between different bosses (so each
of the bosses has its own log) breaks the addon, and it stops recording some 
mechanics. Avoid it for now.


### Requirements/dependencies

- Unicode_table.py: this script is imported and used to draw the table around
the data
- pyperclip: automatically copies the table in the clipboard. Not required.
- win32api/pywin32: used for a faster processing of logs for different bosses.
It can be installed with pip install pywin32. Not required.

The mechanics log plugin can be found at
http://martionlabs.com/arcdps-mechanics-log-plugin/

If you have comments, questions, remarks or suggestions about this script,
please contact me on Discord (Aikan#4668) or in-game (Aikan.5674).
