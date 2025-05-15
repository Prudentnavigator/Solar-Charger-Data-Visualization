#!/bin/env python3
# -*- mode: python; coding: utf-8 -*-

# Script by Thomas Pirchmoser (tommy_software@mailfence.com) 2024

# This script was created for personal/educational purposes only and is not to
#   be used for commercial or profit purposes.

'''
custom_nav_toolbar.py -- Class to customize the NavigationToolbar2Tk of
Matplolib by creating a subclass of it and overriding some methods.
'''

import os
from typing import override
import tkinter as tk
import numpy as np
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk


class CustomNavigationToolbar(NavigationToolbar2Tk):
    """
    Custom Navigation Toolbar.

    This toolbar adds additional functionality and customizes the
    existing tools.
    """

    # Override the toolitems to add or modify buttons
    toolitems = (
                (None, None, None, None),
                ('Pan',
                 'Left button pans, Right button zooms\n'
                 'x/y fixes axis, CTRL fixes aspect',
                 'move', 'pan'),
                (None, None, None, None),
                ('Back', 'Back to previous view',
                 'back_arrow_2', 'back'),
                ('Home', 'Original view',
                 'home', 'home'),
                ('Forward', 'Forward to next view',
                 'forward_arrow_2', 'forward'),
                (None, None, None, None),
                ('Zoom', 'Zoom to rectangle\nx/y fixes axis',
                 'zoom_to_rect', 'zoom'),
                (None, None, None, None),
                ('Save', 'Save this chart',
                 'filesave', 'save_figure'),
                (None, None, None, None)
                )

    def __init__(self, canvas, window, pack_toolbar=False):
        super().__init__(canvas, window, pack_toolbar=False)

    @override
    def _Spacer(self):
        '''
        Overrides the spacer of the buttons of the navtoolbar.
        '''
        s = tk.Frame(master=self, height='20p', relief=tk.RIDGE, bg="#3771a9")
        s.pack(side=tk.LEFT, padx='10p')
        return s

    @override
    def _set_image_for_button(self, button):
        """
        Set the image for a button based on its pixel size.

        The pixel size is determined by the DPI scaling of the window.
        """
        if button._image_file is None:
            return

        # Allow _image_file to be relative to the app's "images" data
        # directory rather than Matplotlib's.
        file_dir = os.path.dirname(os.path.dirname(__file__)) + "/images/"
        image_file = button._image_file.replace(
                            "/usr/share/matplotlib/mpl-data/images/", "")

        path_regular = file_dir + image_file

        size = button.winfo_pixels('20p')

        # Nested functions because ToolbarTk calls  _Button.
        def _get_color(color_name):
            # `winfo_rgb` returns an (r, g, b) tuple in the range 0-65535
            return button.winfo_rgb(button.cget(color_name))

        def _is_dark(color):
            if isinstance(color, str):
                color = _get_color(color)
            return max(color) < 65535 / 2

        def _recolor_icon(image, color):
            image_data = np.asarray(image).copy()
            black_mask = (image_data[..., :3] == 0).all(axis=-1)
            image_data[black_mask, :3] = color
            return Image.fromarray(image_data, mode="RGBA")

        # Use the high-resolution (48x48 px) icon if it exists and is needed
        with Image.open(path_regular) as im:
            # assure a RGBA image as foreground color is RGB
            im = im.convert("RGBA")
            image = ImageTk.PhotoImage(im.resize((size, size)), master=self)
            button._ntimage = image

            # create a version of the icon with the button's text color
            foreground = (255 / 65535) * np.array(
                button.winfo_rgb(button.cget("foreground")))
            im_alt = _recolor_icon(im, foreground)
            image_alt = ImageTk.PhotoImage(
                im_alt.resize((size, size)), master=self)
            button._ntimage_alt = image_alt

        if _is_dark("background"):
            # For Checkbuttons, we need to set `image` and `selectimage` at
            # the same time. Otherwise, when updating the `image` option
            # (such as when changing DPI), if the old `selectimage` has
            # just been overwritten, Tk will throw an error.
            image_kwargs = {"image": image_alt}
        else:
            image_kwargs = {"image": image}
        # Checkbuttons may switch the background to `selectcolor` in the
        # checked state, so check separately which image it needs to use in
        # that state to still ensure enough contrast with the background.
        if (
            isinstance(button, tk.Checkbutton)
            and button.cget("selectcolor") != ""
        ):
            if self._windowingsystem != "x11":
                selectcolor = "selectcolor"
            else:
                # On X11, selectcolor isn't used directly for indicator-less
                # buttons. See `::tk::CheckEnter` in the Tk button.tcl source
                # code for details.
                r1, g1, b1 = _get_color("selectcolor")
                r2, g2, b2 = _get_color("activebackground")
                selectcolor = ((r1+r2)/2, (g1+g2)/2, (b1+b2)/2)
            if _is_dark(selectcolor):
                image_kwargs["selectimage"] = image_alt
            else:
                image_kwargs["selectimage"] = image

        button.configure(**image_kwargs, height='30p', width='30p')

    @override
    def _Button(self, text, image_file, toggle, command):
        '''
        Overrides some values like (borderwidth, background color,
        relieve) etc., of the _Button() from NavigationToolbar2Tk.
        '''
        if not toggle:
            b = tk.Button(
                master=self,
                text=text,
                command=command,
                relief="raised",
                overrelief="groove",
                bg="#3771a9",
                borderwidth=4,
            )
        else:
            # There is a bug in tkinter included in some python 3.6 versions
            # that without this variable, produces a "visual" toggling of
            # other near checkbuttons
            # https://bugs.python.org/issue29402
            # https://bugs.python.org/issue25684
            var = tk.IntVar(master=self)
            b = tk.Checkbutton(
                master=self, text=text, command=command, indicatoron=False,
                variable=var, offrelief="raised", overrelief="groove",
                bg="#3771a9",
                borderwidth=4,
            )
            b.var = var
        b._image_file = image_file
        if image_file is not None:
            # Explicit class because ToolbarTk calls _Button.
            CustomNavigationToolbar._set_image_for_button(self, b)
        else:
            b.configure(font=self._label_font)
        b.pack(side=tk.LEFT)
        return b
