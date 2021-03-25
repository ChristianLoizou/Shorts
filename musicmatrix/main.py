from os import path
from sys import exit, platform
from tkinter import *
from tkinter.ttk import Button, Label, LabelFrame


class Application:
    def __init__(self, width=800, height=600):
        self.version = 'v0.1'
        self.window = Tk()
        self.window.title(f"Music Matrix {self.version}")
        self.window.geometry(f"{width}x{height}")
        self.window.resizable(False, False)
        try: self.window.tk.call('wm', 'iconphoto', self.window._w, PhotoImage(file=f'assets{os.sep}icon.png'))
        except: pass
        self.window.after(500, self.window.focus_force)
    
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    application = Application()
    try:
        from application_update import execute_update
        if execute_update('musicmatrix', application.version, path.basename(__file__)):
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
    application.run()
    
