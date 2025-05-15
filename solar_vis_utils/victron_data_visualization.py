#!/bin/env python3
# -*- mode: python; coding: utf-8 -*-

# Script by Thomas Pirchmoser (tommy_software@mailfence.com) 2024

# This script was created for personal/educational purposes only and is not to
#   be used for commercial or profit purposes.

''' This module retrieves and plots Victron solar history data
from the victron SolarHistory.csv
'''

import datetime as dt
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import dates as mdates

try:
    import solar_history as sh
    from solar_vis_logging import solar_vis_log

except ModuleNotFoundError:
    import solar_vis_utils.solar_history as sh
    from solar_vis_utils.solar_vis_logging import solar_vis_log


logger = solar_vis_log(__name__)


class PlotData:
    ''' Plots solar history. '''

    def __init__(self, day, data, bar_width):
        self.day = day
        self.data = data
        self.bar_width = bar_width

    def plot_daylight(self) -> None:
        ''' Plots total time of solar energy produced. '''
        plt.plot(self.day,
                 get_daylight(self.data),
                 color='orange',
                 linewidth=1,
                 label='Available daylight [min]')

    def plot_solar_yield(self) -> None:
        ''' Plots the yield produced in watthours. '''

        plt.plot(self.day,
                 get_solar_yield(self.data),
                 color='green',
                 linewidth=2,
                 label='Yield [Wh]')

    def plot_max_power(self) -> None:
        ''' Plots the maximum power of the PV in watts. '''

        plt.plot(self.day,
                 get_max_power(self.data),
                 color='blue',
                 linewidth=2,
                 label='Max power [W]')

    def plot_bulk_charge(self) -> None:
        ''' Plots the bulk charge stage in minutes. '''

        plt.bar(self.day,
                get_bulk_charge(self.data),
                width=self.bar_width,
                color='lightgrey',
                edgecolor='black',
                label='Bulk charge [min]')

    def plot_absorption_charge(self) -> None:
        ''' Plots the absorption charge stage in minutes. '''

        plt.bar(self.day,
                get_absorption_charge(self.data),
                width=self.bar_width,
                bottom=get_bulk_charge(self.data),
                edgecolor='black',
                color='grey',
                label='Absorption charge [min]')

    def plot_float_charge(self) -> None:
        ''' Plots the float charge stage in minutes. '''

        bulk_absortion = np.add(get_bulk_charge(self.data),
                                get_absorption_charge(self.data))
        plt.bar(self.day,
                get_float_charge(self.data),
                width=self.bar_width,
                bottom=bulk_absortion,
                color='lightgreen',
                label='Float charge [min]')

    def plot_charge_stages(self) -> None:
        ''' Plots all charge stages in minutes. '''

        PlotData.plot_bulk_charge(self)
        PlotData.plot_absorption_charge(self)
        PlotData.plot_float_charge(self)

    def plot_pv_max_voltage(self) -> None:
        ''' Plots the maximum voltage of the PV panel(s). '''

        plt.plot(self.day,
                 get_pv_max_voltage(self.data),
                 color='brown',
                 linewidth=1,
                 label='Max PV voltage [V]')

    def plot_battery_max_voltage(self) -> None:
        ''' Plots the maximum voltage of the battery bank. '''

        plt.plot(self.day,
                 get_battery_max_voltage(self.data),
                 color='green',
                 linewidth=1,
                 label='Max battery voltage [V]')

    def plot_battery_min_voltage(self) -> None:
        ''' Plots the minimum voltage of the battery bank. '''

        plt.plot(self.day,
                 get_battery_min_voltage(self.data),
                 color='red',
                 linewidth=1,
                 label='Min battery voltage [V]')

    def plot_charger_load_consump(self) -> None:
        ''' Plots the charger load consumption in watthours. '''

        plt.plot(self.day,
                 get_charger_load_consump(self.data),
                 color='purple',
                 linewidth=2,
                 label='Charger load consumption [Wh]')


def get_csv_data() -> dict:
    ''' Returns victron charge data history. '''
    data = sh.victron_charger_history()
    return data


def get_daylight(solar_data: dict) -> list:
    ''' Returns total time of solar production. '''
    return solar_data["daylight"]


def get_solar_yield(solar_data: dict) -> list:
    ''' Returns solar yield '''
    return solar_data["solar_yield"]


def get_charger_load_consump(solar_data: dict) -> list:
    ''' Returns charger load consumption. '''
    return solar_data["charger_load_consump"]


def get_max_power(solar_data: dict) -> list:
    ''' Returns the maximum power of the solar panels produced. '''
    return solar_data["max_power"]


def get_pv_max_voltage(solar_data: dict) -> list:
    ''' Returns the maximum voltage of the solar panels. '''
    return solar_data["pv_max_voltage"]


def get_battery_max_voltage(solar_data: dict) -> list:
    ''' Returns the maximum battery voltage. '''
    return solar_data["battery_max_voltage"]


def get_battery_min_voltage(solar_data: dict) -> list:
    ''' Returns the minimum battery voltage. '''
    return solar_data["battery_min_voltage"]


def get_bulk_charge(solar_data: dict = None) -> list:
    ''' Returns the time of the bulk charge stage. '''
    return solar_data["bulk_charge"]


def get_absorption_charge(solar_data: dict) -> list:
    ''' Returns the time of the absorption charge stage. '''
    return solar_data["absorption_charge"]


def get_float_charge(solar_data: dict) -> list:
    ''' Returns the time of the float charge stage. '''
    return solar_data["float_charge"]


def main() -> None:
    ''' When the module is executed on it's own,
        display a chart of all plots. '''

    data = get_csv_data()

    dates = data["dates"]
    day = [dt.datetime.strptime(d, '%m/%d/%y').date() for d in dates]

    style = plt.style.available[6]
    plt.style.use(style)

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%y'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator())

    plt.gcf().autofmt_xdate()

    bar_width = 0.5

    plot = PlotData(day, data, bar_width)

    # Plot solar data
    PlotData.plot_charge_stages(plot)
    PlotData.plot_daylight(plot)
    PlotData.plot_solar_yield(plot)
    PlotData.plot_max_power(plot)
    PlotData.plot_pv_max_voltage(plot)
    PlotData.plot_battery_max_voltage(plot)
    PlotData.plot_battery_min_voltage(plot)
    PlotData.plot_charger_load_consump(plot)

    s_yield = get_solar_yield(get_csv_data())
    total_yield = sum(s_yield)
    total = f'Total Yield {total_yield / 1000} Kwh'

    plt.xlabel(total, size=15, color='green')

    plt.grid(axis='y', which="major", color='grey')
    plt.grid(axis='x', which="major", color='grey', alpha=0.4)
    plt.grid(axis='y', which="minor", color='grey', alpha=0.4)
    plt.minorticks_on()

    plt.tight_layout()
    plt.title('Solar Charger Data Visualization',
              fontstyle='italic',
              size=20,
              pad=0.5)

    plt.legend(loc='upper right')

    plt.show()


if __name__ == "__main__":
    main()
