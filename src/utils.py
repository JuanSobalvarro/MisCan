import sys
import os

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and PyInstaller """
    try:
        # PyInstaller sets this attribute to the temp folder where resources are unpacked
        base_path = sys._MEIPASS
    except AttributeError:
        # When running normally, use the current file directory
        base_path = os.path.abspath(os.path.dirname(__file__))

    return os.path.join(base_path, relative_path)
