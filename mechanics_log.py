#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
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
"""

import os
import sys
try:
    import pyperclip
    print("Warning: this script will erase the clipboard content\n")
    clipboard = True
except ModuleNotFoundError:
    print("With the pyperclip module installed, this script copies the table in the clipboard so it can directly be pasted in Discord\n")
    clipboard = False

from Unicode_table import make_table

# log directory
DIR = "{}/Documents/Guild Wars 2/addons/arcdps/arcdps.mechanics".format(
    os.environ["USERPROFILE"])
# expected csv headers
HEADERS = [
    'Player Name', 'Account Name',
    'Boss Name', 'Mechanic Name',
    'Neutral', 'Failed', 'Downs', 'Deaths', 'Pulls'
    ]
# list of bosses, used to sort them
BOSSES = [
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
    
    Used to sort them
    """
    for i, boss in enumerate(BOSSES):
        if name == boss:
            return i
    return 0

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
            data.append({key: elem for key, elem in zip(HEADERS, line.strip().split(','))})
    f.close()
    return data

def process_log(file):
    """
    Process a log and return a table made Unicode box characters
    """
    try:
        data = load_log(file)
    except AssertionError:
        print("The log file isn't correctly formatted")
        return ""
    
    # get the relevant boss name
    s_bosses = set([databit["Boss Name"] for databit in data])-set(["All"])
    if len(s_bosses) == 1:
        one_boss = True
        boss_name = s_bosses.pop()
        print("Only boss fight found: {}".format(boss_name))
    else:
        one_boss = False
        l_bosses = sorted(list(s_bosses), key=find_boss_position)
        d_names = {k: v for (k, v) in enumerate(l_bosses, 1)}
        print("More than one boss fight is registered in this log.")
        for k, v in d_names.items():
            print("{:>2}: {}".format(k, v))
        choice = input("For which boss should the mechanics table be built?  ")
        boss_name = d_names[int(choice)]

    # get the list of mechanics to monitor
    choice = input("Include neutral mechanics (y/anything else)?  ")
    if choice == "y":
        neutral = True
    else:
        neutral = False
    s_mechanics_f = set()
    s_mechanics_n = set()
    for databit in data:
        if databit["Boss Name"] == boss_name:
            if databit["Failed"] != "":
                s_mechanics_f.add(databit["Mechanic Name"])
            if databit["Neutral"] != "" and neutral:
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
                                 for databit in data])))
    # d_players is where the data will be stored before being put in a list
    d_players = {p: {m: 0 for m in l_mechanics} for p in l_players}
    # get characters name. Can be used to change the table layout
    for databit in data:
        d_players[databit["Account Name"]]["Player Name"] = \
            databit["Player Name"]

    # fill the player database
    # pulls, failed and neutral mechanics
    for databit in data:
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
    # number of times downed, if relevant
    if one_boss:
        for databit in data:
            if databit["Boss Name"] == "All":
                p_name = databit["Account Name"]
                d_players[p_name]["was downed"] = databit["Downs"]
    # remove players that were not involved in the fight. If they joined for
    # another boss, they'll still be in the log
    for p in l_players:
        if sum([d_players[p][m] for m in l_mechanics]) == 0:
            l_players.remove(p)

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
    caption += "({}): pulls (might not be accurate)\n".format(current_index)
    
    return "```\nMechanics log for {}:\n\n{}\n{}```".format(
        boss_name, table, caption)

if __name__ == "__main__":
    os.chdir(DIR)
    if len(sys.argv) == 1:
        log = input("Type the name of the file to parse.\nIf empty, the script will parse the most recent log.\n")
        if log == "":
            log = find_latest_log()
        if log not in os.listdir():
            input("File could not be found")
            raise ValueError("Wrong filename")
    else:
        log = sys.argv[1]
    print("Processing log {}\n".format(log))
    table = process_log(log)
    if clipboard:
        pyperclip.copy(table)
    print(table.strip("```"))
    input("Hit return to close")





