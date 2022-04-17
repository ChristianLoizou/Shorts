import os
from tkinter import *


class Application(Tk):
    def __init__(self, version):
        self.version = version
        super().__init__()
        self.title(f"Intonation Trainer {self.version}")
        self.geometry("800x600")
        self.resizable(False, False)
        try:
            self.tk.call('wm', 'iconphoto', self._w,
                         PhotoImage(file=f'assets{os.sep}icon.png'))
        except:
            pass
        self.after(500, self.focus_force)


if __name__ == "__main__":
    __version__ = 'v0.1'

    try:
        from application_update import execute_update
        if execute_update('intonationtrainer', __version__, os.path.basename(__file__)):
            exit()
    except ModuleNotFoundError:
        pass

    application = Application(__version__)
    application.mainloop()
