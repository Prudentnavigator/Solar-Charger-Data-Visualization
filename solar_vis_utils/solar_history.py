#!/bin/env python3
# -*- mode: python; coding: utf-8 -*-

# Script by Thomas Pirchmoser (tommy_software@mailfence.com) 2024

# This script was created for personal/educational purposes only and is not to
#   be used for commercial or profit purposes.

'''
A module that extracts data from the solarhistory.csv file and
  and stores that data in a dictionary.
'''

import os

try:
    from solar_vis_logging import solar_vis_log

except ModuleNotFoundError:
    from solar_vis_utils.solar_vis_logging import solar_vis_log

logger = solar_vis_log(__name__)

parent_dir = os.path.dirname(os.path.dirname(__file__))
csv = f"{parent_dir}/solarhistory.csv"


def victron_charger_history() -> dict:
    ''' Extract data and store in the "solar_data" dictionary. '''

    solar_data = {
                  "dates": [],
                  "daylight": [],
                  "solar_yield": [],
                  "charger_load_consump": [],
                  "max_power": [],
                  "pv_max_voltage": [],
                  "battery_min_voltage": [],
                  "battery_max_voltage": [],
                  "bulk_charge": [],
                  "absorption_charge": [],
                  "float_charge": []
                  }

    with open(csv, "r", encoding="utf-8") as infile:

        csv_header = True

        try:
            for row in infile:
                col = row.split(",")

                if not csv_header:
                    solar_data["dates"].append(col[0])

                    total_time_min = int(col[7]) + int(col[8]) + int(col[9])
                    total_time = total_time_min
                    solar_data["daylight"].append(total_time)
                    solar_data["solar_yield"].append(int(col[1]))
                    solar_data["charger_load_consump"].append(int(col[2]))
                    solar_data["max_power"].append(float(col[3]))
                    solar_data["pv_max_voltage"].append(float(col[4]))
                    solar_data["battery_min_voltage"].append(float(col[5]))
                    solar_data["battery_max_voltage"].append(float(col[6]))
                    solar_data["bulk_charge"].append(round(int(col[7])))
                    solar_data["absorption_charge"].append(round(int(col[8])))
                    solar_data["float_charge"].append(round(int(col[9])))

                csv_header = False

        except IndexError:
            pass

    return solar_data
