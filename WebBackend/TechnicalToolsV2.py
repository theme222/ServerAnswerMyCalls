"""
This is the Technical tools python library created for general purpose stuff
just so you know I have no idea what half of this means so don't ask
"""

from random import randint, choice
from inspect import currentframe, getframeinfo
import os
import hashlib

show_filename = False
show_line_number = False


def log(message, logtitle="info", var=None, color="blue"):
    """
    printing but with color!
    :param message:
    :param var:
    :param logtitle:
    :param var:
    :param color:
    """
    if var is not None:
        var = '|' + str(var) + '|'
    else:
        var = ""

    linenumber = currentframe().f_back.f_lineno
    if os.name == 'nt':
        filename = getframeinfo(currentframe().f_back).filename.split('\\')[-1]
    else:
        filename = getframeinfo(currentframe().f_back).filename.split('/')[-1]

    color_codes = {"black": 30, "red": 31, "green": 32, "yellow": 33, "blue": 34, "purple": 35, "cyan": 36, "white": 37}
    try:
        color = color_codes[color]
    except KeyError:
        log("Color not found", logtitle="error", color="red")
        color = 36

    filenametxt = ""
    linenumbertxt = ""
    if show_filename:
        filenametxt = f"in {filename} "
    if show_line_number:
        linenumbertxt = f"at line {linenumber} "
    print_message = f'\033[1;{color}m[{logtitle.upper()}] {filenametxt}{linenumbertxt}- {message} {var}\033[0m'
    print(print_message)


def time_convert(seconds):
    """
    turns absurd amounts of seconds into understandable text
    :param seconds:
    :return:
    """

    year = 31557600
    month = 2629800
    week = 604800
    day = 86400
    hour = 3600
    minute = 60
    second = 1
    millisecond = 0.001
    microsecond = 0.000001
    nanosecond = 0.000000001

    return_text = ''

    amount = seconds // year
    if amount > 0:
        return_text = return_text + f' {int(amount)} Year'
        seconds -= year * amount

    amount = seconds // month
    if amount > 0:
        return_text = return_text + f' {int(amount)} Month'
        seconds -= month * amount

    amount = seconds // week
    if amount > 0:
        return_text = return_text + f' {int(amount)} Week'
        seconds -= week * amount

    amount = seconds // day
    if amount > 0:
        return_text = return_text + f' {int(amount)} Day'
        seconds -= day * amount

    amount = seconds // hour
    if amount > 0:
        return_text = return_text + f' {int(amount)} Hour'
        seconds -= hour * amount

    amount = seconds // minute
    if amount > 0:
        return_text = return_text + f' {int(amount)} Minute'
        seconds -= minute * amount

    amount = seconds // second
    if amount > 0:
        return_text = return_text + f' {int(amount)} Second'
        seconds -= second * amount

    amount = int(seconds / millisecond)
    if amount > 0:
        return_text = return_text + f' {amount} MilliSecond'
        seconds -= millisecond * amount

    amount = int(seconds / microsecond)
    if amount > 0:
        return_text = return_text + f' {amount} MicroSecond'
        seconds -= microsecond * amount

    amount = int(seconds / nanosecond)
    if amount > 0:
        return_text = return_text + f' {amount} NanoSecond'
        seconds -= nanosecond * amount

    return return_text + ' '


def color_gen(style='rgb'):
    """ Makes a random color depending on style """
    color_names = ['blue', 'orange', 'green', 'red', 'purple', 'brown', 'pink', 'gray', 'cyan', 'black',
                   'magenta', 'yellow', 'aqua', 'purple', 'pink']
    if style == 'rgb' or style == 'RGB':
        return [randint(0, 255), randint(0, 255), randint(0, 255)]
    elif style == 'hex':
        return '#' + format(randint(0, 16777215), 'x')
    elif style == 'name' or style == 'color':
        return choice(color_names)


class TextFile:
    """Simple class to format text files"""

    def __init__(self):
        pass

    def __repr__(self):
        return 'Why would you do this?'

    @staticmethod
    def delnewline(filename, char_amount):
        """Deletes a set number of characters after a new line"""
        finishedtext = ''
        for line in open(filename, 'r'):
            finishedtext += line[char_amount:]
        filename_new = filename.split('.')[0] + '_new.txt'
        try:
            open(filename_new, 'x').write(finishedtext)
        except FileExistsError:
            log('error', 'Created file already exists', filename_new)

    @staticmethod
    def replaceword(filename, word, replacement=''):
        """finds the word and replaces with another thing"""
        finishedtext = ''
        for line in open(filename, 'r'):
            finishedtext += line.replace(word, replacement)
        filename_new = filename.split('.')[0] + '_new.txt'
        try:
            open(filename_new, 'x').write(finishedtext)
        except FileExistsError:
            log('error', 'Created file already exists', filename_new)


def multi_delete(list_, args):
    args = set(args)
    indexes = sorted(args, reverse=True)
    for index in indexes:
        del list_[index]
    return list_

# From https://unogeeks.com/python-sha256/
def sha256(data):
    # Convert data to bytes if it’s not already
    if isinstance(data, str):
        data = data.encode()

    # Calculate SHA-256 hash
    sha256_hash = hashlib.sha256(data).hexdigest()

    return sha256_hash


if __name__ == '__main__':
    log("aaadsffasd")
