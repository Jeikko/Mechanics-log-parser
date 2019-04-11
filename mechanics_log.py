#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
Parse the Martion Laboratories mechanics log into a Discord-friendly table


Description:

The arcdps mechanics plugin records a log of all mechanics happening
throughout a raid run. This script loads it, looks for the information related
to a given boss and puts it in a table made from Unicode characters, so it can
be pasted on Discord using the code (```code```) environment. If the pyperclip
Python module is available, the code (including the ```) will directly be
copied into the clipboard.

To quote Martion Labs: "This plugin is not intended to breed toxicity, but
instead help show players mechanical areas where the players can improve. This
is in the same way that arcdps shows how dps/boons could be improved."
The purpose of this script is to help with this, by turning that information
into a table that can be easily read by everyone.


How to use this script:

There are three ways of loading a log:
♦ in the Windows explorer, drop the log on the python script
♦ launch the script, enter the log name
♦ launch the script and simply hit return. The latest log will be parsed

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


Remarks:

As of 2019-04-09, the plugin creates the log file only after the gw2 client is
closed. This can be overriden by opening the mechanics chart window
(Alt+Shift+N) and clicking "export".

The log includes mechanics for all the bosses encountered while the gw2 client
was running. As a consequence, the created table will encompass all the
attempts on a given boss. The "pull" column should reflect that number of
attempts. It should tell if players only came for some attempts.

It also records a single "was downed" number for all of the fights, so if
different bosses are fought, there is no way of telling how many times a
player was downed on a specific encounter.

It seems that hitting "export" and "reset" between different bosses (so each
of the bosses has its own log) breaks the addon, and it stops recording some 
mechanics. Avoid it for now.


Requirements/dependencies
♦ Unicode_table.py: this script is imported and used to draw the table around
the data
♦ pyperclip: automatically copies the table in the clipboard. Not required.
♦ win32api/pywin32: used for a faster processing of logs for different bosses.
It can be installed with pip install pywin32. Not required.

The mechanics log plugin can be found at
http://martionlabs.com/arcdps-mechanics-log-plugin/

If you have comments, questions, remarks or suggestions about this script,
please contact me on Discord (Aikan#4668) or in-game (Aikan.5674).
"""

import os
import sys
import configparser
import time

try:
    import pyperclip
    print("Warning: this script will erase the clipboard content\n")
    clipboard = True
except ModuleNotFoundError:
    print("With the pyperclip module installed, this script copies the table" +
    " in the clipboard\nso it can directly be pasted in Discord\n")
    clipboard = False

try:
    import win32api
    has_win32api = True
    try:
        config = configparser.ConfigParser()
        config.read("mechanics_log_settings.ini")
        if config.has_section("Config"):
            hold_key = int(config["Config"]["HoldingKey"], 16)
        else:
            config["Config"] = {}
            raise KeyError
    except KeyError:
        hold_key = 0x56
        config["Config"]["HoldingKey"] = "0x56"
        with open("mechanics_log_settings.ini", 'w') as configfile:
            config.write(configfile)
except ModuleNotFoundError:
    has_win32api = False

from Unicode_table import make_table

# expected csv headers
HEADERS = [
    'Player Name', 'Account Name',
    'Boss Name', 'Mechanic Name',
    'Neutral', 'Failed', 'Downs', 'Deaths', 'Pulls'
    ]
# list of bosses, used to sort them
BOSSES = [
    "FotM Generic", "MAMA", "Siax", "Ensolyss of the Endless Torment", "Arkk",
    "Vale Guardian", "Gorseval the Multifarious", "Sabetha the Saboteur",
    "Slothasor", "Matthias Gabrel",
    "Keep Construct", "Xera",
    "Cairn the Indomitable", "Samarog", "Deimos",
    "Soulless Horror", "Statues - Soul Eater", "Dhuum",
    "Conjured Amalgamate", "Twin Largos", "Qadim",
    ]

def find_boss_position(name):
    """
    Find the position of a given boss in the above table
    """
    for i, boss in enumerate(BOSSES):
        if name == boss:
            return i
    return 0

def hold_script():
    """
    Put the script on hold until a signal from the user
    
    If win32api is available, the signal is the press and release of a given
    key, that can happen outside of the Python window. If not, the signal is
    the user hitting return in that window
    """
    if has_win32api:
        while win32api.GetKeyState(hold_key) not in [-128, -127]:
            time.sleep(0.01)
        while win32api.GetKeyState(hold_key) in [-128, -127]:
            time.sleep(0.01)
    else:
        input("Hit return to proceed to the next boss")


def get_log_directory():
    """
    Look for the log directory in a config file, create it if needed
    """
    try:
        config = configparser.ConfigParser()
        config.read("mechanics_log_settings.ini")
        if config.has_section("Config"):
            return config["Config"]["LogDirectory"]
        else:
            config["Config"] = {}
            raise KeyError
    except KeyError:
        while True:
            dir = input("Please enter the arcdps mechanics log folder, " + 
            "for example\nC:\\Users\\Username\\Documents\\GUILD WARS 2" +
            "\\addons\\arcdps\\arcdps.mechanics\n> ").strip()
            if os.path.exists(dir):
                print()
                break
            else:
                print("The directory doesn't exist\n")
        config["Config"]["LogDirectory"] = dir
        with open("mechanics_log_settings.ini", 'w') as configfile:
            config.write(configfile)
        return dir


def get_ctime(filename):
    """
    Return the creation time of a file
    
    Used to sort them
    """
    return os.stat(filename).st_ctime

def find_latest_log():
    log = sorted(os.listdir(), key=lambda file:get_ctime(file))[-1]
    return log

def load_log(name):
    """
    Load a log into a list of data bits
    """
    f = open(name)
    assert f.readline().strip().split(',') == HEADERS
    data = []
    for line in f.readlines():
        data.append({key: elem for key, elem in zip(
                                HEADERS, line.strip().split(','))})
    f.close()
    return data

def get_boss_names(file):
    """
    Process a log and get the list of bosses the user is interested in
    """
    try:
        data = load_log(file)
    except AssertionError:
        print("The log file isn't correctly formatted")
        return ""
    
    s_bosses = set([databit["Boss Name"] for databit in data])-set(["All"])
    if len(s_bosses) == 1:
        boss_names = [s_bosses.pop()]
        print("Only boss fight found: {}".format(boss_names[0]))
        return boss_names
    elif len(s_bosses) == 0:
        print("That log is empty")
        return []
    else:
        l_bosses = sorted(list(s_bosses), key=find_boss_position)
        d_names = {k: v for (k, v) in enumerate(l_bosses, 1)}
        print("More than one boss fight is registered in this log.")
        for k, v in d_names.items():
            print("{:>2}: {}".format(k, v))
        choice = input("Type the number of the boss for which " + 
            "the mechanics table should be built.\n" +
            "You can enter several numbers, separated by commas: ")
        boss_names = [d_names[int(c.strip())] for c in choice.split(',')]
        print("Processing {}".format(', '.join(boss_names)))
        return boss_names

def process_log(file, boss_name):
    """
    Process a log and return a table made Unicode box characters
    """
    try:
        data = load_log(file)
    except AssertionError:
        print("The log file isn't correctly formatted")
        return ""
    
    # check whether the was_downed stat can be used
    s_bosses = set([databit["Boss Name"] for databit in data])-set(["All"])
    if len(s_bosses) == 1:
        one_boss = True
    else:
        one_boss = False
    
    # get the list of mechanics to monitor
    s_mechanics_f = set()
    s_mechanics_n = set()
    for databit in data:
        if databit["Boss Name"] == boss_name:
            if databit["Failed"] != "":
                s_mechanics_f.add(databit["Mechanic Name"])
            if databit["Neutral"] != "":
                s_mechanics_n.add(databit["Mechanic Name"])
    # list of failed mechanics
    l_mechanics_f = sorted(list(s_mechanics_f))
    # downs are not relevant if the log is about different boss fights
    if one_boss:
        l_mechanics_f.append("was downed")
    # list of neutral mechanics
    l_mechanics_n = sorted(list(s_mechanics_n))
    # all mechanics and pulls, will make the header of the table
    l_mechanics = l_mechanics_n + l_mechanics_f + ["Pulls"]
    
    
    # get the list of players
    l_players = sorted(list(set([databit["Account Name"]
                                 for databit in data
                                 if databit["Boss Name"] == boss_name])))
    # d_players is where the data will be stored before being put in a list
    d_players = {p: {m: 0 for m in l_mechanics} for p in l_players}
    # get characters name. Can be used to change the table layout
    for databit in data:
        try:
            d_players[databit["Account Name"]]["Player Name"] = \
                databit["Player Name"]
    # if some players joined for another boss, they'll be in the log but not
    # in l_players. Ignore them
        except KeyError:
            pass
    
    
    # fill the player database
    # pulls, failed and neutral mechanics
    for databit in data:
        try:
            m_name = databit["Mechanic Name"]
            p_name = databit["Account Name"]
            if databit["Boss Name"] == boss_name:
                d_players[p_name]["Pulls"] = int(databit["Pulls"])
                if m_name in l_mechanics:
                    if databit["Failed"] != "":
                        nb = int(databit["Failed"])
                    elif databit["Neutral"] != "":
                        nb = int(databit["Neutral"])
                    d_players[p_name][m_name] = nb
        except KeyError:
            pass
    # number of times downed, if relevant
    if one_boss:
        for databit in data:
            if databit["Boss Name"] == "All":
                p_name = databit["Account Name"]
                d_players[p_name]["was downed"] = databit["Downs"]
    
    
    # create the table
    table_data = [["Account Name"] +
                  ["({})".format(i) 
                    for i, m in enumerate(l_mechanics, 1)]]
    for p in l_players:
        table_data.append([p.strip(":")] +
                          [d_players[p][m] for m in l_mechanics])
    # table formatting
    # horizontal lines
    h_lines = "02{}2".format((len(l_players)-1)*"0")
    # vertical lines. The account name, neutral mechanics, failed mechanics
    # and pull parts of the table will be separated by a thick line
    if l_mechanics_n != []:
        neutral_bit = "{}2".format((len(l_mechanics_n)-1)*"1")
    else:
        neutral_bit = ""
    if l_mechanics_f != []:
        failed_bit = "{}2".format((len(l_mechanics_f)-1)*"1")
    else:
        print("No failed mechanics")
        failed_bit = ""
    v_lines = "02{}{}2".format(neutral_bit, failed_bit)
    # create table
    table = make_table(table_data, v_lines, h_lines)

    # caption
    caption = ""
    current_index = 1
    if l_mechanics_n != []:
        caption += "♦ Neutral mechanics:\n"
        for i, m in enumerate(l_mechanics_n, current_index):
            caption += "({}): {}\n".format(i, m)
        current_index += len(l_mechanics_n)
    if l_mechanics_f != []:
        caption += "♦ Failed mechanics:\n"
        for i, m in enumerate(l_mechanics_f, current_index):
                caption += "({}): {}\n".format(i, m)
        current_index += len(l_mechanics_f)
    else:
        caption += "♦ No failed mechanic recorded\n"
    caption += "♦ Others:\n"
    caption += ("({}): number of attempts" + 
        " (might not be accurate)\n").format(current_index)
    
    return "```\nMechanics log for {}:\n\n{}\n{}```".format(
        boss_name, table, caption)

if __name__ == "__main__":
    # get the name of the file to process
    if len(sys.argv) == 1:
        dir = get_log_directory()
        os.chdir(dir)
        log = input("Type the name of the file to parse" +
        " (including the .csv, but the directory\nisn't needed)." + 
        " If empty, the script will parse the most recent log.\n> ")
        if log == "":
            log = find_latest_log()
        if log not in os.listdir():
            input("File could not be found")
            raise ValueError("Wrong filename")
    else:
        log = sys.argv[1]
    print("Processing log {}\n".format(log))
    
    # process bosses and display
    boss_names = get_boss_names(log)
    print()
    if not clipboard:
        print("Reminder: right-clicking in a Windows terminal copies" + 
            " the selected text in the clipboard")
    if has_win32api and len(boss_names) > 1:
        print("To move to the next log processing, press and release the" + 
            " V key\n(pasting using ctrl+V in Discord triggers it, but" +
            " the key can be\nmodified in mechanics_log_settings.ini)")
    while boss_names:
        table = process_log(log, boss_names.pop(0))
        if clipboard:
            pyperclip.copy(table)
        print()
        print(table)
        if boss_names:
            hold_script()
            print()
    input("Hit return to close")





