"""csv2json module"""

import logging
import os

logging.basicConfig(filename="console.log", filemode='w', level=logging.INFO)

def get_logger(module_name: str):
    """return custom logger"""
    logger = logging.getLogger(module_name)
    return logger
