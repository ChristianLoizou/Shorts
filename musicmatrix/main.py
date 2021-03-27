#!python3.7
import numpy as np
from os import path, sep
from random import choice as randchoice
from sys import exit, platform
from tkinter import *
from tkinter import font
from tkinter.ttk import Label, LabelFrame, Button as ttkButton
from tkinter.messagebox import askyesno
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
        self._cellwidth, self._cellheight = None, None
        self._frame_pad = 25
        self._minimum_gridsize = 2
        self._maximum_gridsize = 15
        self._default_gridsize = 5
        self._gridsize = self._default_gridsize
        self._currently_selected = None
        self._font = "Verdana" if "Verdana" in font.families() else None
        self.keys = {
            'control': False,
            'alt': False   
        }

        self.window.config(background=COLORS['WINDOW_BACKGROUND'])
        self.window.bind('<KeyPress>', partial(self.callbacks.key_pressed, self))
        self.window.bind('<KeyRelease>', partial(self.callbacks.key_released, self))
        self.window.title(f"Music Matrix {self.version}")
        self.window.geometry(f"{self._width}x{self._height}")
        self.window.resizable(False, False)
        self.window.tk.call('wm', 'iconphoto', self.window._w, PhotoImage(file=f'assets{sep}icon.png'))
        
        self.cells = [[Cell() for _ in range(self._gridsize)] for _ in range(self._gridsize)]
        self._mainframe = Frame(self.window, width=self._width, height=3*self._height//4)
        self._buttonframe = Frame(self.window, width=self._width, height=self._height//4)
        self.create_grid()
        self.draw_window()
        self.window.after(500, self.window.focus_force)
    
    def run(self):
        self.window.mainloop()
    
    def draw_window(self):
        self.update_cell_display()
        self.create_menubuttons()
        self._mainframe.place(x=self._frame_pad, y=self._frame_pad)
        self._buttonframe.place(
            x=self._frame_pad + (self._mainframe['width']//4), 
            y=self._mainframe['height'] + (self._frame_pad*2)
            )
    
    def create_grid(self):
        self._grid_buttons = list()
        self._mainframe.destroy()
        self._mainframe = Frame(self.window, width=self._width, height=3*self._height//4)
        self._cellwidth = (self._mainframe['width'] - (4*self._frame_pad)) // (self._gridsize + 1)
        self._cellheight = (self._mainframe['height'] - (4*self._frame_pad)) // (self._gridsize + 1)
        
        Label(
            self._mainframe, 
            text='P0 →',
            font=(self._font, 18)
        ).place(
            x=(-.15*self._cellwidth)+self._frame_pad, 
            y=(.5*self._cellheight)+self._frame_pad, 
            width=self._cellwidth, 
            height=self._cellheight
        )
        for rn, r in enumerate(self.cells):
            self._grid_buttons.append(list())
            for cn, c in enumerate(r):
                cbtn = Button(
                    self._mainframe, 
                    text=c.content,
                    font=(self._font, 24),
                    command=partial(self.callbacks.gridbutton, self, cn, rn),
                    highlightbackground=COLORS['BTNBG_NOTSELECTED']
                    )
                cbtn.place(
                    x=((rn+.5)*self._cellwidth)+self._frame_pad, 
                    y=((cn+.5)*self._cellheight)+self._frame_pad, 
                    width=self._cellwidth, 
                    height=self._cellheight
                    )
                self._grid_buttons[-1].append(cbtn)

    def update_cell_display(self):
        for rn, r in enumerate(self._grid_buttons):
            for cn, b in enumerate(r):
                self._grid_buttons[rn][cn].config(
                    text=self.cells[rn][cn].content,
                    highlightbackground=COLORS['BTNBG_NOTSELECTED']
                )
        if self._currently_selected is not None:
            if self._currently_selected[0] >= self._gridsize:
                self._currently_selected = (self._gridsize-1, self._currently_selected[1])
            if self._currently_selected[1] >= self._gridsize:
                self._currently_selected = (self._currently_selected[0], self._gridsize-1)
            x, y = self._currently_selected
            self._grid_buttons[x][y].config(highlightbackground=COLORS['BTNBG_SELECTED'])
    
    
    def create_menubuttons(self):
        btn_export       = ttkButton(self._buttonframe, text="Export to MIDI",      command=partial(self.callbacks.export,              self))
        btn_increase     = ttkButton(self._buttonframe, text="Increase grid size",  command=partial(self.callbacks.increase_gridsize,   self))
        btn_decrease     = ttkButton(self._buttonframe, text="Decrease grid size",  command=partial(self.callbacks.decrease_gridsize,   self))
        btn_cleargrid    = ttkButton(self._buttonframe, text="Clear grid",          command=partial(self.callbacks.cleargrid,           self))
        btn_completegrid = ttkButton(self._buttonframe, text="Complete grid",       command=partial(self.callbacks.completegrid,        self))
        btn_settings     = ttkButton(self._buttonframe, text="Settings",            command=partial(self.callbacks.settings,            self))


        btn_export.grid      (row=0, column=0, columnspan=2, sticky='nsew')
        btn_increase.grid    (row=1, column=0,               sticky='nsew')
        btn_decrease.grid    (row=1, column=1,               sticky='nsew')
        btn_cleargrid.grid   (row=2, column=0,               sticky='nsew')
        btn_completegrid.grid(row=2, column=1,               sticky='nsew')
        btn_settings.grid    (row=3, column=0, columnspan=2, sticky='nsew')


    class callbacks:
        def gridbutton(self, x, y):
            # c = self.cells[y][x]
            self._currently_selected = (y, x)
            self.update_cell_display()
            
        def export(self):
            pass
        
        def increase_gridsize(self):
            if self._gridsize < self._maximum_gridsize:
                self._gridsize += 1
                ncells = [[Cell() for _ in range(self._gridsize)] for _ in range(self._gridsize)]
                for rn in range(len(self.cells)):
                    for cn in range(len(self.cells[rn])):
                        try:
                            ncells[rn][cn].content = self.cells[rn][cn].content
                        except:
                            pass
                self.cells = ncells
                self._cellwidth = (self._mainframe['width'] - (2*self._frame_pad)) // self._gridsize
                self._cellheight = (self._mainframe['height'] - (2*self._frame_pad)) // self._gridsize
                self.create_grid()
                self.draw_window()
        
        def decrease_gridsize(self):
            if self._gridsize > self._minimum_gridsize:
                self._gridsize -= 1
                ncells = [[Cell() for _ in range(self._gridsize)] for _ in range(self._gridsize)]
                for rn in range(len(self.cells)):
                    for cn in range(len(self.cells[rn])):
                        try:
                            ncells[rn][cn].content = self.cells[rn][cn].content
                        except:
                            pass
                self.cells = ncells
                self._cellwidth = (self._mainframe['width'] - (2*self._frame_pad)) // self._gridsize
                self._cellheight = (self._mainframe['height'] - (2*self._frame_pad)) // self._gridsize
                self.create_grid()
                self.draw_window()
        
        def settings(self):
            settings_popup = Toplevel()
            settings_popup.title('Settings')
            
            settings_popup.mainloop()
        
        def key_pressed(self, event):
            if self._currently_selected is not None:
                y, x = self._currently_selected
                if event.char == event.keysym and event.char.lower() in 'abcdefg':
                    self.cells[y][x].content = event.char.upper()
                    if self.keys['control']: self.cells[y][x].content += 'b'
                    elif self.keys['alt']: self.cells[y][x].content += '#'
                elif event.keysym in ['Right', 'Left', 'Up', 'Down']:
                    dx, dy = {'Right':(0,1), 'Left':(0,-1), 'Up':(-1,0), 'Down':(1,0)}[event.keysym]
                    if 0 <= y+dy < self._gridsize and 0 <= x+dx < self._gridsize:
                        self._currently_selected = (y+dy, x+dx)
                elif event.keysym == 'BackSpace':
                    self.cells[y][x].content = "_"
                elif 'Control' in event.keysym or 'Meta' in event.keysym:
                    self.keys['control'] = True
                elif 'Alt' in event.keysym or 'Shift' in event.keysym:
                    self.keys['alt'] = True
                elif event.keysym == 'Escape':
                    self._currently_selected = None
            print(event.keysym)
            self.update_cell_display()

        def key_released(self, event):
            if 'Control' in event.keysym or 'Meta' in event.keysym:
                self.keys['control'] = False
            elif 'Alt' in event.keysym or 'Shift' in event.keysym:
                self.keys['alt'] = False
        
        def completegrid(self):
            sure = askyesno(
                'Are you sure?', 
                'Completing the grid will erase data all but the prime row (P0). Are you sure you want to continue?'
                )
            if sure:
                pass #complete the grid from P0
            else:
                return

        def cleargrid(self):
            for r in self.cells:
                for c in r:
                    c.content = "_"
            self.update_cell_display()

if __name__ == "__main__":
            
    if platform in ["win32", 'linux']:
        COLORS = {
            "WINDOW_BACKGROUND": '#cccccc',
            "TEXTCOLOR": 'black',
            "BTNBG_NOTSELECTED": '#3E4149',
            "BTNBG_SELECTED": '#4074E1'

        }
    elif platform == "darwin":
        COLORS = {
            "WINDOW_BACKGROUND": 'systemWindowBackgroundColor',
            "TEXTCOLOR": 'systemTextColor',
            "BTNBG_NOTSELECTED": 'systemWindowBackgroundColor',
            "BTNBG_SELECTED": '#4074E1'

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
