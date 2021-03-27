from os import path
from sys import platform
from tkinter import *
from tkinter.ttk import Button as ttkButton, Frame, Label


class Application:
    def __init__(self, version, width=500, height=500):
        self.version = version
        self._width, self._height = width, height

        self.window = Tk()
        self.window.title(f'Text to Midi {self.version}')
        self.window.geometry(f"{self._width}x{self._height}")
        self.window.config(bg=COLORS['WINDOW_BACKGROUND'])

        self.setup_window()

    def run(self):
        self.window.mainloop()
    
    def setup_window(self):
        return

if __name__ == "__main__":

    __version__ = 'v0.1'

    try:
        from application_update import execute_update
        if execute_update('texttomidi', __version__, path.basename(__file__)):
            exit()
    except ModuleNotFoundError:
        pass

    if platform in ["win32", 'linux']:
        COLORS = {
            "WINDOW_BACKGROUND": '#cccccc',
            "TEXTCOLOR": 'black'

        }
    elif platform == "darwin":
        COLORS = {
            "WINDOW_BACKGROUND": 'systemWindowBackgroundColor',
            "TEXTCOLOR": 'systemTextColor'

        }

    application = Application(__version__)
    application.run()
