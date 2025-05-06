#!/bin/env python3
# -*- mode: python; coding: utf-8 -*-

# Script by Thomas Pirchmoser (tommy_software@mailfence.com) 2024

# This script was created for personal/educational purposes only and is not to
#   be used for commercial or profit purposes.

'''
Module to modify a newly added Victron SolarHistory.csv and merge
  it with the solarhistory.csv.
'''

import os
import tkinter as tk
from datetime import datetime

try:
    from solar_vis_logging import solar_vis_log
except ModuleNotFoundError:
    from solar_vis_utils.solar_vis_logging import solar_vis_log

logger = solar_vis_log(__name__)

suffix = datetime.now().strftime("%m%d%Y")


def archive_csv(add_csv: str) -> None:
    ''' Creates a backup of the new CSV file. '''
    try:
        with open(add_csv, "r", encoding="utf-8") as infile:
            archive = f"./History/Archive/SolarHistory{suffix}.csv"
            with open(archive, "w", encoding="utf-8") as backup_file:
                for row in infile:
                    backup_file.write(row)

            logger.debug(" SolarHistory.csv has been archived!")

    except FileNotFoundError:
        logger.warning(" SolarHistory.csv does not exist!")
        tk.messagebox.showerror("Error!", "File does not exist.\
                                    Please add a SolarHistory.csv\
                                    to the History Folder!")

    else:
        alter_solarhistory_csv(add_csv)
        merge_solarhistory_csv(WRITE_CSV, TMP_CSV)


def alter_solarhistory_csv(add_csv: str) -> None:
    ''' Read the SolarHistory.csv and remove the 'Days ago' column. '''

    with open(add_csv, "r", encoding="utf-8") as infile:
        rows = []

        for line in infile:
            index = line.find(",")
            rows.append(line[index + 1:])

        # Rewrite the altered SolarHistory.csv
        with open(TMP_CSV, "w", encoding="utf=8") as tmp_file:
            for row in rows:
                tmp_file.write(f'{row}')


def merge_solarhistory_csv(csv: str, tmp_csv: str) -> None:
    ''' Combine the newly SolarHistory.csv with the previous csv. '''

    with open(csv, "r", encoding="utf-8") as f_1, \
         open(tmp_csv, "r", encoding="utf-8") as f_2:
        file1 = f_1.readlines()
        file2 = f_2.readlines()

    with open(csv, "w", encoding="utf-8") as out:
        for line in file2:
            if line in file1:
                out.write(line)
            else:
                out.write(line)

    with open(csv, "a+", encoding="utf-8") as out:
        for line in file1:
            if line not in file2:
                out.write(line)

        tk.messagebox.showinfo("Success!",
                               "solar data has been added")

        logger.debug(" SolarHistory.csv has been added to solarhistory.csv!")

        os.remove("./History/tmp.csv")


def add_solarhistory_csv(add_csv: str) -> None:
    ''' Add a new csv file to the existing solarhistory data '''

    archive_csv(add_csv)


TMP_CSV = "./History/tmp.csv"
WRITE_CSV = "solarhistory.csv"
