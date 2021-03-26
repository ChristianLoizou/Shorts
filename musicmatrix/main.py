from os import path, sep
from sys import exit, platform
from tkinter import *
from tkinter import font
from tkinter.ttk import Label, LabelFrame
from functools import partial

class Application:
    def __init__(self, version, width=800, height=800):
        self.window = Tk()
        self.version = version
        self._width, self._height = width, height
        self._frame_pad = 15
        self._minimum_gridsize = 2
        self._maximum_gridsize = 20
        self._default_gridsize = 5
        self._gridsize = self._default_gridsize
        self._cellsize = min([self._width, self._height]) - self._frame_pad
        self._font = "Verdana" if "Verdana" in font.families() else None

        self.window.config(background=COLORS['WINDOW_BACKGROUND'])
        self.window.title(f"Music Matrix {self.version}")
        self.window.geometry(f"{self._width}x{self._height}")
        self.window.resizable(False, False)
        try: self.window.tk.call('wm', 'iconphoto', self.window._w, PhotoImage(file=f'assets{sep}icon.png'))
        except: pass
        self.setup_window()
        self.window.after(500, self.window.focus_force)
    
    def run(self):
        self.window.mainloop()
    
    def setup_window(self):
        self._mainframe = Frame(self.window, width=self._width, height=self._height, borderwidth=1)
        self.cells = [[str(i+j) for i in range(self._gridsize)] for j in range(self._gridsize)]
        self.display_cells()
        self._mainframe.pack(padx=self._frame_pad, pady=self._frame_pad)
    
    def display_cells(self):
        for rn, r in enumerate(self.cells):
            for cn, s in enumerate(r):
                btn = Button(self._mainframe, text=s, width=5, height=5, command=partial(print, cn, rn, s))
                btn.grid(row=cn, column=rn)
                

if __name__ == "__main__":
            
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
        

    __version__ = 'v0.1'

    try:
        from application_update import execute_update
        if execute_update('musicmatrix', __version__, path.basename(__file__)):
            exit()
    except ModuleNotFoundError:
        pass
    application = Application(__version__)
    application.run()
