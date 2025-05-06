#!/bin/env python3
# -*- mode: python; coding: utf-8 -*-

# Script by Thomas Pirchmoser (tommy_software@mailfence.com) 2024

# This script was created for personal/educational purposes only and is not to
#   be used for commercial or profit purposes.

'''
app_logging.py--set up the logging for client.py.
'''

import os
import logging
from logging import handlers

parent_dir = os.path.dirname(os.path.dirname(__file__))
log_file = f"{parent_dir}/.solar_vis.log"


def solar_vis_log(name: str) -> logging.Logger:
    ''' Set-up the logging object. '''

    # Get current logger instance with name of the module.
    logger = logging.getLogger(name)

    # Set log level to debug - higher than info.
    logger.setLevel(logging.DEBUG)

    # Create a formatter object with specified format for the logs.
    formatter = logging.Formatter(
                            '%(asctime)s:%(levelname)s:%(name)s:%(message)s',
                            "%Y-%m-%d %H:%M:%S")

    # Create file handler to handle log files rotation and backup.
    file_handler = handlers.RotatingFileHandler(log_file,
                                                maxBytes=30000,
                                                backupCount=1)

    # Set formatter for the file handler object.
    file_handler.setFormatter(formatter)

    # Add file handler to logger instance.
    logger.addHandler(file_handler)

    return logger


# Calling the function and logging a message.
if __name__ == "__main__":
    log = solar_vis_log(__name__)
    log.info("[TEST] logging is set up.")
