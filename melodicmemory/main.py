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
        self.setup_widgets()

    def setup_widgets(self):
        self.menu = Menu(self)
        self.config(menu=self.menu)
        self.filemenu = Menu(self.menu)
        self.filemenu.add_command(
            label="Settings", command=self.settings_popup
        )
        self.filemenu.add_command(
            label="Information", command=self.information_popup
        )
        self.filemenu.add_command(label="Exit", command=self.on_exit)
        self.menu.add_cascade(menu=self.filemenu, label='File')

        self.mainframe = Frame(self)
        self.lblframe_opts = LabelFrame(
            self.mainframe,
            text='Choose the odd one out')
        self.frame_btns = Frame(self.mainframe)

        self.options = [
            Button(self.lblframe_opts,
                   text='1',
                   command=lambda: self.option(1)),
            Button(self.lblframe_opts,
                   text='2',
                   command=lambda: self.option(2)),
            Button(self.lblframe_opts,
                   text='3',
                   command=lambda: self.option(3)),
        ]

        self.btn_play = Button(self.frame_btns,
                               text='Play exercise',
                               command=self.play_ex)
        self.btn_reveal = Button(self.frame_btns,
                                 text='Reveal answer',
                                 command=self.reveal_ex)
        for btn in self.options:
            btn.pack(side='left', fill='both', expand=True)
        self.lblframe_opts.pack(fill='both', expand=True, pady=10)
        self.btn_play.pack(fill='x', expand=True, ipady=5)
        self.btn_reveal.pack(fill='x', expand=True, ipady=5)
        self.frame_btns.pack(fill='both', expand=True, pady=10)
        self.mainframe.pack(fill='both', expand=True)

    def settings_popup(self):
        return

    def information_popup(self):
        return

    def on_exit(self):
        self.destroy()
        self.quit()

    def option(self, option):
        print(option)

    def play_ex(self):
        print("Exercise playing...")

    def reveal_ex(self):
        print("Exercise revealed")


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
