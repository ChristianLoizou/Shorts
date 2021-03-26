import numpy as np
from os import path, sep
from random import choice as randchoice
from sys import exit, platform
from tkinter import *
from tkinter import font
from tkinter.ttk import Label, LabelFrame, Button as ttkButton
from functools import partial

class Cell:
    def __init__(self, content='_'):
        self.content = content
    
    def __repr__(self):
        return f"<Cell object - content: {self.content}>"

class Application:
    def __init__(self, version, width=800, height=900):
        self.window = Tk()
        self.version = version
        self._width, self._height = width, height
        self._frame_pad = 25
        self._minimum_gridsize = 2
        self._maximum_gridsize = 20
        self._default_gridsize = 5
        self._gridsize = self._default_gridsize
        self._font = "Verdana" if "Verdana" in font.families() else None

        self.window.config(background=COLORS['WINDOW_BACKGROUND'])
        self.window.title(f"Music Matrix {self.version}")
        self.window.geometry(f"{self._width}x{self._height}")
        self.window.resizable(False, False)
        try: self.window.tk.call('wm', 'iconphoto', self.window._w, PhotoImage(file=f'assets{sep}icon.png'))
        except: pass
        self.cells = [[Cell() for _ in range(self._gridsize)] for _ in range(self._gridsize)]
        self.draw_window()
        self.window.after(500, self.window.focus_force)
    
    def run(self):
        self.window.mainloop()
    
    def draw_window(self):
        try: 
            self._mainframe.destroy()
            self._buttonframe.destroy()
        except: 
            pass
        self._mainframe = Frame(self.window, width=self._width, height=3*self._height//4)
        self._buttonframe = Frame(self.window, width=self._width, height=self._height//4)
        self.update_cell_display()
        self.create_menubuttons()
        self._mainframe.place(x=self._frame_pad, y=self._frame_pad)
        self._buttonframe.place(
            x=self._frame_pad + (self._mainframe['width']//4), 
            y=self._mainframe['height'] + (self._frame_pad*2)
            )
    
    def update_cell_display(self):
        cellwidth = (self._mainframe['width'] - (2*self._frame_pad)) // self._gridsize
        cellheight = (self._mainframe['height'] - (2*self._frame_pad)) // self._gridsize
        for rn, r in enumerate(self.cells):
            for cn, c in enumerate(r):
                cbtn = Button(
                    self._mainframe, 
                    text=c.content,
                    command=partial(self.callbacks.gridbutton, self, cn, rn)
                    )
                cbtn.place(x=(rn*cellwidth), y=(cn*cellheight), width=cellwidth, height=cellheight)

    
    def create_menubuttons(self):
        btn_export   = ttkButton(self._buttonframe, text="Export to MIDI",      command=partial(self.callbacks.export,              self))
        btn_increase = ttkButton(self._buttonframe, text="Increase grid size",  command=partial(self.callbacks.increase_gridsize,   self))
        btn_decrease = ttkButton(self._buttonframe, text="Decrease grid size",  command=partial(self.callbacks.decrease_gridsize,   self))
        btn_settings = ttkButton(self._buttonframe, text="Settings",            command=partial(self.callbacks.settings,            self))

        btn_increase.grid(row=1, column=0,               sticky='nsew')
        btn_decrease.grid(row=1, column=1,               sticky='nsew')
        btn_export.grid  (row=0, column=0, columnspan=2, sticky='nsew')
        btn_settings.grid(row=2, column=0, columnspan=2, sticky='nsew')

    class callbacks:
        def gridbutton(self, x, y):
            c = self.cells[y][x]

            self.update_cell_display()
            
        
        def export(self):
            pass
        
        def increase_gridsize(self):
            if self._gridsize < self._maximum_gridsize:
                self._gridsize += 1
                arr = np.array(self.cells, dtype=Cell)
                arr = np.resize(arr, [self._gridsize, self._gridsize])
                self.cells = np.where(arr==0, Cell(), arr)
                self.draw_window()
        
        def decrease_gridsize(self):
            if self._gridsize > self._minimum_gridsize:
                self._gridsize -= 1
                arr = np.array(self.cells, dtype=Cell)
                arr = np.resize(arr, [self._gridsize, self._gridsize])
                self.cells = np.where(arr==0, Cell(), arr)
                self.draw_window()
        
        def settings(self):
            pass

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
