"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
"""
import re


def rem_tab_space(line):
    """
    :method: Deletes all leading and trailing edges from a string.
    :param line: The string to be cleaned.
    :returns: Cleaned string.
    """

    value = re.sub(r'^\s+|\s+$', '', line)
    return value


def rem_tab_space_quot(line):
    """
    :method: Removes from a string all leading, trailing spaces
             tabs and quotations.
    :param line: The string to be cleaned.
    :returns: Cleaned string.
    """
    line = rem_tab_space(line)
    line = re.sub(r'^\"+|\"+$', '', line)
    return line


def split_line(line):
    """
    :method: Splits lines with multiple values into a list of values
             delimiters could be spaces and tabs.
    :param line: The line to be split.
    :returns: A list of values.
    """
    line = rem_tab_space(line)  # remove leading and trailing waste
    values = re.split(r'[\t\s]\s*', line)
    return values


def chk_num(val, ret=0):
    """
    :method: Checks if a value is integer, float or a string containing
             a numerical value.
    :param val: The value to check.
    :param ret: Optional parameter defining what must be returned
                if val is not numerical.
    :returns: If val is numerical: val, else  0 or ret.
    """
    if isinstance(val, int) or isinstance(val, float):
        return val
    elif val.isnumeric():
        return val
    else:
        return ret


def chk_str(val, ret='x'):
    """
    :method: Checks if a value is string and the length is > 0.
    :param val: The value to check.
    :param ret: Optional parameter defining what must be returned if
                val is not string or empty.
    :returns: If val is non-empty string: val, else  x or ret.
    """
    if isinstance(val, str) and len(val) > 0:
        return val
    else:
        return ret


class FileHelpers(object):
    """
    :class: little helpers for file reading and writing all over.
    """

    __className = 'FileHelpers'
    '''
    :attr: Does help to indicate the source of the log messages.
    '''

    def __init__(self):
        """
        Constructor
        """
