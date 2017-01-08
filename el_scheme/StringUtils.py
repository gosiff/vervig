import re
import os
import sys
from datetime import datetime


def parse_image_filename(filename):
    regxp = re.search(r'(left|right)_(\d{8})_(\d{4})_.*', os.path.basename(filename))

    if regxp is not None:
        timestr = regxp.group(2)[:4] + "-" + regxp.group(2)[4:6] + "-" + regxp.group(2)[6:] + " " + \
                  regxp.group(3)[:2] + ":" + regxp.group(3)[2:]

        dt = datetime.strptime(timestr, "%Y-%m-%d %H:%M")

        return regxp.group(1), dt

    return None, None


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)