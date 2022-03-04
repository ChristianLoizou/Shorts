from os import path, sep
from tkinter import *
from tkinter import messagebox


class Application(Tk):
    def __init__(self, version, *args, **kwargs):
        super(Application, self).__init__(*args, **kwargs)
        self.version = version
        self.title(f"MelodicMemory {self.version}")
        self.geometry('300x300+150+150')
        self.resizable(False, False)
        self.tk.call('wm', 'iconphoto', self._w,
                     PhotoImage(file=f'assets{sep}icon.png'))


if __name__ == "__main__":
    __version__ = "v0.1"

    try:
        from application_update import execute_update
        if execute_update('melodicmemory', __version__, path.basename(__file__)):
            exit()

    except ModuleNotFoundError:
        pass

    application = Application(__version__)
    application.after(500, application.focus_force)
    application.mainloop()
