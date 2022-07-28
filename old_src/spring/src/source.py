import pandas as pd
import re

def get_lab_nums(answers):
    """

    :param df:
    :return:
    """
    return [list(re.findall(r'(\d+\.\d+)', x)) if isinstance(x, str) else [str(x)] for x in answers ]

def get_nums(answers):
    """

    :param df:
    :return:
    """
    return [list(re.findall(r'(\d+)', x)) if isinstance(x, str) else [str(x)] for x in answers]