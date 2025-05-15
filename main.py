#!/bin/env python3
# -*- mode: python; coding: utf-8 -*-

# Script by Thomas Pirchmoser (tommy_software@mailfence.com) 2024

# This script was created for personal/educational purposes only and is not to
#   be used for commercial or profit purposes.

'''
Gui application for visualizing Victron Charger SolarHistory.
'''

import os
import tkinter as tk
# from tkinter import simpledialog
from tkinter import filedialog
import datetime as dt
from matplotlib import pyplot as plt
from matplotlib import dates as mdates
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from ui.custom_navtoolbar import CustomNavigationToolbar
import solar_vis_utils.victron_data_visualization as vdv
from solar_vis_utils.victron_data_visualization import PlotData
from solar_vis_utils import csv_due
import solar_vis_utils.mod_solarhistory as ms
from solar_vis_utils.solar_vis_logging import solar_vis_log

logger = solar_vis_log(__name__)


class SolarPlotter:
    ''' GUI solar data plotter class. '''

    win = None
    toolbar = None

    def __init__(self, plot, bar_width):
        self.plot = plot
        self.bar_width = bar_width

        self.widget = {
                       "menu_button": None,
                       "yield_button": None,
                       "daylight_button": None,
                       "pv_max_power_button": None,
                       "charge_stages_button": None,
                       "pv_max_voltage_button": None,
                       "battery_max_voltage_button": None,
                       "battery_min_voltage_button": None,
                       "charger_load_consump": None,
                       "clear_plot_button": None,
                       "plot_data_canvas": None,
                       "add_csv_button": None,
                       "daily_consumption_label": None
                       }

        self.chart = {
                      "fig": None,
                      "plot_ax": None,
                      "canvas": None
                      }

        self.create_gui()

    def create_gui(self):
        ''' Method to create the GUI'''

        SolarPlotter.win = tk.Tk()
        self.win.title('Solar Charger Data Visualization')
        self.win.config(bg='#3771a9')

        self.win.resizable(1, 1)
        self.win.columnconfigure(index=10, weight=1)
        self.win.rowconfigure(index=2, weight=3)

        self.gui_buttons()

        self.gui_labels()

        self.data_canvas()

        self.gui_layout()

        self.draw_plot()

        # Function to be called when user chooses to close the window.
        self.win.protocol("WM_DELETE_WINDOW", close_app)

        logger.info("[GUI]: has been created...")

        self.win.mainloop()

    def gui_buttons(self) -> None:
        ''' Initiate buttons '''

        bt_1 = tk.Button(self.win,
                         state="normal",
                         text="PV yield",
                         activebackground="#3771a9",
                         activeforeground="white",
                         fg='blue',
                         bd=3,
                         relief="raised",
                         command=self.plot_solar_yield)

        self.widget["yield_button"] = bt_1

        bt_2 = tk.Button(self.win,
                         state="normal",
                         text="Daylight",
                         activebackground="#3771a9",
                         activeforeground="white",
                         fg='blue',
                         bd=3,
                         relief="raised",
                         command=self.plot_daylight)

        self.widget["daylight_button"] = bt_2

        bt_3 = tk.Button(self.win,
                         state="normal",
                         text="PV max power",
                         activebackground="#3771a9",
                         activeforeground="white",
                         fg='blue',
                         bd=3,
                         relief="raised",
                         command=self.plot_max_power)

        self.widget["pv_max_power_button"] = bt_3

        bt_4 = tk.Button(self.win,
                         state="normal",
                         text="Charge stages",
                         activebackground="#3771a9",
                         activeforeground="white",
                         fg='blue',
                         bd=3,
                         relief="raised",
                         command=self.plot_charge_stages)

        self.widget["charge_stages_button"] = bt_4

        bt_5 = tk.Button(self.win,
                         state="normal",
                         text="PV max voltage",
                         activebackground="#3771a9",
                         activeforeground="white",
                         fg='blue',
                         bd=3,
                         relief="raised",
                         command=self.plot_pv_max_voltage)

        self.widget["pv_max_voltage_button"] = bt_5

        bt_6 = tk.Button(self.win,
                         state="normal",
                         text="Battery max voltage",
                         activebackground="#3771a9",
                         activeforeground="white",
                         fg='blue',
                         bd=3,
                         relief="raised",
                         command=self.plot_battery_max_voltage)

        self.widget["battery_max_voltage_button"] = bt_6

        bt_7 = tk.Button(self.win,
                         state="normal",
                         text="Battery min voltage",
                         activebackground="#3771a9",
                         activeforeground="white",
                         fg='blue',
                         bd=3,
                         relief="raised",
                         command=self.plot_battery_min_voltage)

        self.widget["battery_min_voltage_button"] = bt_7

        bt_8 = tk.Button(self.win,
                         state="normal",
                         text='Charger load consumption',
                         activebackground="#3771a9",
                         activeforeground="white",
                         fg='blue',
                         bd=3,
                         command=self.plot_charger_load_consump)

        self.widget["charger_load_consump"] = bt_8

        bt_9 = tk.Button(self.win,
                         state="normal",
                         text="clear plot",
                         activebackground="#3771a9",
                         activeforeground="white",
                         fg='blue',
                         bd=3,
                         relief="raised",
                         command=self.clear_plot)

        self.widget["clear_plot_button"] = bt_9

        bt_10 = tk.Button(self.win,
                          state="normal",
                          text='add data',
                          activebackground="#3771a9",
                          activeforeground="white",
                          fg='blue',
                          bd=3,
                          command=self.add_csv)

        self.widget["add_csv_button"] = bt_10

    def gui_labels(self) -> None:
        ''' Creates GUI labels. '''

        s_yield = vdv.get_solar_yield(vdv.get_csv_data())
        daily_consumption_average = round(sum(s_yield) / len(s_yield))
        average = f"Average daily consumption: {daily_consumption_average}Wh"

        self.widget["daily_consumption_label"] = tk.Label(self.win,
                                                          bg="#3771a9",
                                                          font=20,
                                                          text=average)

    def data_canvas(self):
        ''' Place matplotlib background into a canvas. '''

        self.chart["fig"] = plt.figure()
        self.chart["ax"] = plt.axes()
        self.chart["canvas"] = FigureCanvasTkAgg(figure=self.chart["fig"],
                                                 master=self.win)

        self.widget["plot_data_canvas"] = self.chart["canvas"].get_tk_widget()

    def gui_layout(self):
        ''' Layout widgets. '''

        self.widget["daylight_button"].grid(row=0,
                                            column=0,
                                            padx=25,
                                            pady=10,
                                            sticky="E")

        self.widget["yield_button"].grid(row=0,
                                         column=1,
                                         sticky='WE',
                                         padx=15,
                                         pady=10)

        self.widget["pv_max_power_button"].grid(row=0,
                                                column=2,
                                                padx=15,
                                                pady=10)

        self.widget["charge_stages_button"].grid(row=0,
                                                 column=3,
                                                 padx=15,
                                                 pady=10)

        self.widget["pv_max_voltage_button"].grid(row=0,
                                                  column=4,
                                                  padx=15,
                                                  pady=10)

        self.widget["battery_max_voltage_button"].grid(row=0,
                                                       column=5,
                                                       padx=15,
                                                       pady=10)

        self.widget["battery_min_voltage_button"].grid(row=0,
                                                       column=6,
                                                       padx=15,
                                                       pady=10)

        self.widget["charger_load_consump"].grid(row=0,
                                                 column=7,
                                                 sticky="W",
                                                 padx=15,
                                                 pady=10)

        self.widget["clear_plot_button"].grid(row=0,
                                              column=13,
                                              padx=40,
                                              pady=10,
                                              sticky="E")

        self.widget["add_csv_button"].grid(row=0,
                                           column=14,
                                           padx=20,
                                           pady=10,
                                           sticky="E")

        self.widget["plot_data_canvas"].grid(row=1,
                                             column=0,
                                             columnspan=15,
                                             sticky="NSWE",
                                             rowspan=6,
                                             padx=10,
                                             pady=5)

        self.widget["daily_consumption_label"].grid(row=7,
                                                    column=0,
                                                    columnspan=2,
                                                    padx=20,
                                                    pady=10)

    def draw_plot(self) -> None:
        ''' Plot the solar data. '''

        style = plt.style.available[4]
        plt.style.use(style)

        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%y'))
        plt.gca().xaxis.set_major_locator(mdates.DayLocator())

        plt.gcf().autofmt_xdate()

        s_yield = vdv.get_solar_yield(vdv.get_csv_data())
        total_yield = sum(s_yield)
        total = f'Total Yield {total_yield / 1000} Kwh'

        plt.xlabel(total, size=15, color='#3771a9')

        plt.grid(axis='y', which="major", color='grey')
        plt.grid(axis='x', which="major", color='grey', alpha=0.4)
        plt.grid(axis='y', which="minor", color='grey', alpha=0.4)
        plt.minorticks_on()

        plt.tight_layout()

        plt.legend(loc='upper right')
        self.chart["canvas"].draw()

        self.chart["canvas"].get_tk_widget().grid(row=1, column=0)

        self.create_nav_toolbar()

    def create_nav_toolbar(self) -> None:
        '''
        Creates and displays in the GUI a custom navigation toolbar.
        '''

        self.toolbar = CustomNavigationToolbar(self.chart["canvas"],
                                               self.win,
                                               pack_toolbar=False)

        self.toolbar.grid(row=7,
                          column=4,
                          columnspan=12,
                          sticky="NSEW",
                          pady=5)

        self.toolbar.configure(borderwidth=5,
                               background="#3771a9",
                               relief="flat",
                               bd=0,
                               padx=50,
                               pady=2)

        self.toolbar.update()

        self.toolbar.set_message("Welcome!")

    def clear_plot(self) -> None:
        ''' Clear the chart and reset the buttons. '''

        self.widget["daylight_button"].config(state="normal",
                                              bg="lightgrey",
                                              fg="blue",
                                              relief="raised")

        self.widget["yield_button"].config(state="normal",
                                           bg="lightgray",
                                           fg="blue",
                                           relief="raised")

        self.widget["pv_max_power_button"].config(state="normal",
                                                  bg="lightgray",
                                                  fg="blue",
                                                  relief="raised")

        self.widget["charge_stages_button"].config(state="normal",
                                                   bg="lightgray",
                                                   fg="blue",
                                                   relief="raised")

        self.widget["pv_max_voltage_button"].config(state="normal",
                                                    bg="lightgray",
                                                    fg="blue",
                                                    relief="raised")

        self.widget["battery_max_voltage_button"].config(state="normal",
                                                         bg="lightgray",
                                                         fg="blue",
                                                         relief="raised")

        self.widget["battery_min_voltage_button"].config(state="normal",
                                                         bg="lightgray",
                                                         fg="blue",
                                                         relief="raised")

        self.widget["charger_load_consump"].config(state="normal",
                                                         bg="lightgray",
                                                         fg="blue",
                                                         relief="raised")

        self.chart["ax"].clear()
        self.draw_plot()
        self.toolbar.update()

        logger.debug("[GUI]: chart has been cleared...")

    def add_csv(self) -> None:
        ''' Add new solar data to solarhistory.csv. '''

        data_file = filedialog.askopenfilename()

        if not data_file:
            return

        ms.add_solarhistory_csv(data_file)
        self.clear_plot()

        data = vdv.get_csv_data()
        logger.debug(" solarhistory.csv loading --> success...")

        dates = data["dates"]
        day = [dt.datetime.strptime(d, '%m/%d/%y').date() for d in dates]

        self.plot = PlotData(day, data, self.bar_width)

    def plot_daylight(self):
        ''' Plot the amount of daylight and reconfigure
            the approriate button. '''

        self.widget["daylight_button"].config(state='disabled',
                                              bg='orange',
                                              disabledforeground='black',
                                              relief='sunken'
                                              )

        PlotData.plot_daylight(self.plot)

        self.draw_plot()

        logger.debug(" daylight has been plotted...")

    def plot_solar_yield(self):
        ''' Plot solar yield and reconfigure the approriate button. '''

        self.widget["yield_button"].config(state='disabled',
                                           relief='sunken',
                                           bg='green',
                                           disabledforeground='black')

        PlotData.plot_solar_yield(self.plot)

        self.draw_plot()

        logger.debug(" solar yield has been plotted...")

    def plot_max_power(self):
        ''' Plot maximum power of the PV and reconfigure
            the approriate button.  '''

        self.widget["pv_max_power_button"].config(state="disabled",
                                                  relief="sunken",
                                                  bg="blue",
                                                  disabledforeground="black")

        PlotData.plot_max_power(self.plot)

        self.draw_plot()

        logger.debug(" max power has been plotted...")

    def plot_charge_stages(self):
        ''' Plot all charge stages and reconfigure the approriate button. '''

        self.widget["charge_stages_button"].config(state="disabled",
                                                   relief="sunken",
                                                   bg="grey",
                                                   disabledforeground="black")

        PlotData.plot_charge_stages(self.plot)

        self.draw_plot()

        logger.debug(" charge stages have been plotted...")

    def plot_pv_max_voltage(self):
        ''' Plot the maximum PV voltage and reconfigure
            the approriate button. '''

        self.widget["pv_max_voltage_button"].config(state="disabled",
                                                    relief="sunken",
                                                    bg="brown",
                                                    disabledforeground="black")

        PlotData.plot_pv_max_voltage(self.plot)

        self.draw_plot()

        logger.debug(" pv max voltage has been plotted...")

    def plot_battery_max_voltage(self):
        ''' Plot the maximum battery voltage and reconfigure
            the approriate button. '''

        self.widget["battery_max_voltage_button"].config(
                                                    state="disabled",
                                                    relief="sunken",
                                                    bg="lightgreen",
                                                    disabledforeground="black"
                                                    )

        PlotData.plot_battery_max_voltage(self.plot)

        self.draw_plot()

        logger.debug(" battery max voltage has been plotted...")

    def plot_battery_min_voltage(self):
        ''' Plot the minimum battery voltage and reconfigure
            the approriate button. '''

        self.widget["battery_min_voltage_button"].config(
                                                     state="disabled",
                                                     relief="sunken",
                                                     bg="red",
                                                     disabledforeground="black"
                                                     )

        PlotData.plot_battery_min_voltage(self.plot)

        self.draw_plot()

        logger.debug(" battery min voltage has been plotted...")

    def plot_charger_load_consump(self):
        ''' Plot the charger load consumption and reconfigure
            the approriate button. '''

        self.widget["charger_load_consump"].config(state="disabled",
                                                   relief="sunken",
                                                   bg="purple",
                                                   disabledforeground="black"
                                                   )

        PlotData.plot_charger_load_consump(self.plot)

        self.draw_plot()

        logger.debug(" charger load consumption has been plotted...")


def check_csv_last_upload():
    ''' Check if more data needs to be added.'''

    urgent, alert = csv_due.time_to_add_csv()

    if alert:
        tk.messagebox.showinfo("Info",
                               "Please add a new SolarHistory.csv\
                                        as soon as possible!")
    if urgent:
        tk.messagebox.showwarning("Warning",
                                  "Please add a new SolarHistory.csv\
                                        to avoid data gaps!")


def close_app():
    ''' When the user clicks the "x" on the top righthand corner
        the program closes. '''

    logger.info("[STOP]: program closed by user...")

    os._exit(0)


def main():
    ''' Main entry point. '''

    logger.info("[START]: program has been started...")

    check_csv_last_upload()

    data = vdv.get_csv_data()

    logger.info(" solarhistory.csv loading --> success!")

    dates = data["dates"]
    day = [dt.datetime.strptime(d, '%m/%d/%y').date() for d in dates]

    style = plt.style.available[4]
    plt.style.use(style)

    bar_width = 0.5

    plots = PlotData(day, data, bar_width)

    SolarPlotter(plots, bar_width)


if __name__ == "__main__":
    main()
