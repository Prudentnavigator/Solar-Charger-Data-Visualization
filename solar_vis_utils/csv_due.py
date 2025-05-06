#!/bin/env python3
# -*- mode: python; coding: utf-8 -*-

# Script by Thomas Pirchmoser (tommy_software@mailfence.com) 2024

# This script was created for personal/educational purposes only and is not to
#   be used for commercial or profit purposes.

'''
This module checks the days passed between the last SolarHistory.csv data that
  was added, and today. As the Victron Charger only stores data up to 29 days,
  it let's the user know if more data needs to be added so as to not have data
  gaps.
'''

import os
from datetime import datetime

try:
    import solar_history as sh
    import mod_solarhistory as mod_history
    from solar_vis_logging import solar_vis_log

except ModuleNotFoundError:
    import solar_vis_utils.solar_history as sh
    from solar_vis_utils import mod_solarhistory as mod_history
    from solar_vis_utils.solar_vis_logging import solar_vis_log

logger = solar_vis_log(__name__)

parent_dir = os.path.dirname(os.path.dirname(__file__))
csv = f"{parent_dir}/solarhistory.csv"


def check_last_update() -> int | dict:
    '''
    Checks for how many days passed since the last
    time data was added.
    '''

    data = sh.victron_charger_history()

    date = datetime.now()

    last_update_day = data["dates"][0][3:5]

    today = date.strftime("%d")
    todays_date = date.strftime("%m/%d/%y")

    logger.debug(" today's date: %s", todays_date)

    try:
        days_ago = int(today) - int(last_update_day)

    except ValueError:
        try:
            last_update_day = data["dates"][0][3:4]
            days_ago = int(today) - int(last_update_day)

        except ValueError:
            last_update_day = data["dates"][0][2:3]
            days_ago = int(today) - int(last_update_day)

    return days_ago, data


def time_to_add_csv() -> bool:
    '''
    This function returns, if days passed exceed 20 days (csv_alert = True)
      or if days passed exceed 25 days (csv_urgent =True), otherwise both
      variables return False.
     '''

    days_ago, data = check_last_update()

    if days_ago < 0:
        days_ago = 31 + days_ago

    logger.debug(" last day data has been added: %s", data['dates'][0])
    logger.debug(" %s days since data has been added.", days_ago)

    csv_alert = False
    csv_urgent = False

    if days_ago >= 25:  # or days_ago >= -5:
        csv_urgent = True
        logger.warning("[Urgent]: SolarHistory.csv needs to be added!")

    elif days_ago >= 20:  # or days_ago >= -10:
        csv_alert = True
        logger.info(" please add SolarHistory.csv soon!")

    return csv_urgent, csv_alert


try:
    file_size = os.path.getsize(csv)

    # The first time the program is run, the solarhistory.csv file will be
    #  empty and data will be added if there is a SolarHistory.csv.
    if file_size <= 2:
        mod_history.add_solarhistory_csv()
        logger.info("[START] solarhistory.csv file -> loaded!")

except FileNotFoundError:
    # If the solarhistory.csv file does not exist, create the csv and add data.
    with open(csv, "w", encoding="utf-8") as first_csv:
        pass

    logger.info("[START] solarhistory.csv file has been created!")

    mod_history.add_solarhistory_csv()

if __name__ == "__main__":
    logger.debug("[TEST] csv_due module test starting...")
    time_to_add_csv()
    logger.debug("[TEST] csv_due module test ending...")
