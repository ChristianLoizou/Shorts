from collections import defaultdict
from functools import partial
from midiutil.MidiFile import MIDIFile
from os import path, sep
from random import choice as ranchoice
from sys import platform
from tkinter import *
from tkinter import font
from tkinter.ttk import Button, Checkbutton, Entry, Frame, Label, Scrollbar


class CustomText(Text):
    def __init__(self, *args, **kwargs):
        Text.__init__(self, *args, **kwargs)

        self._orig = self._w + "_orig"
        self.tk.call("rename", self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)

    def _proxy(self, command, *args):
        cmd = (self._orig, command) + args
        try: result = self.tk.call(cmd)
        except TclError as e: result = None

        if command in ("insert", "delete", "replace"):
            self.event_generate("<<TextModified>>")
        return result

class Application:
    def __init__(self, version, width=500, height=500):
        self.version = version
        self._width, self._height = width, height
        self.window = Tk()
        self.window.title(f'Text to Midi {self.version}')
        self.window.config(bg=COLORS['WINDOW_BACKGROUND'])
        self.window.minsize(width, height)
        self.window.bind('<Configure>', partial(self.callbacks.resize, self))
        self.window.tk.call('wm', 'iconphoto', self.window._w, PhotoImage(file=f'assets{sep}icon.png'))
        self.ipadx, self.ipady = 25, 25
        self._font = "Verdana" if "Verdana" in font.families() else None
        self._fontsize = 18
        self._settings = {
            'auto_sub': IntVar(value=0),
            'complex_tokens': IntVar(value=0)
        }
        self.delimiter = '-'

        self.setup_window()
        self.update_display()

    @property
    def width(self): return self._width
    
    @property
    def height(self): return self._height

    def run(self):
        self.window.mainloop()
    
    def setup_window(self):
        self.widgets = dict()
        self.widgets['text_main'] = (
            CustomText(
                self.window, 
                cursor='text', 
                font=(self._font, self._fontsize)
                ),
            dict(row=0, column=0, columnspan=3, padx=15, pady=15, ipadx=self.ipadx, ipady=self.ipady, sticky='nsew')
        )
        self.widgets['text_main'][0].bind('<<TextModified>>', partial(self.callbacks.data_inputted, self))
        self.widgets['text_main'][0].bind('<<Paste>>', partial(self.callbacks.paste, self))
        self.widgets['btn_convert'] = (
            Button(self.window, text='Convert to Midi', command=partial(self.callbacks.convert, self)),
            dict(row=2, column=0, columnspan=2, ipadx=self.ipadx, padx=self.ipadx, pady=(self.ipady//2, 0), sticky='nsew')
            )
        self.widgets['btn_settings'] = (
            Button(self.window, text='Settings', command=self.settings),
            dict(row=3, column=0, ipadx=self.ipadx, padx=(self.ipadx, 0), pady=(0, self.ipady//2), sticky='nsew')
            )
        self.widgets['btn_help'] = (
            Button(self.window, text='Help', command=self.help),
            dict(row=3, column=1, ipadx=self.ipadx, padx=(0, self.ipadx), pady=(0, self.ipady//2), sticky='nsew')
        )

        for i in range(2):
            self.window.grid_rowconfigure(i,weight=1)
            self.window.grid_columnconfigure(i,weight=1)

        for widget, options in self.widgets.values():
            widget.grid(**options)
        return
    
    def update_display(self):
        for widget, options in self.widgets.values():
            widget.grid_forget()
            widget.grid(**options)
    
    def help(self):
        try: self.help_popup.destroy()
        except: pass
        self.help_popup = Toplevel(self.window)
        self.help_popup.title('Help')
        self.help_popup.geometry('300x300')
        self.help_popup.resizable(False, False)
        self.help_popup.bind('<FocusOut>', lambda _: self.help_popup.destroy())

        Message(self.help_popup, text="").pack(fill='both', expand=True)

        self.help_popup.mainloop()
    
    def settings(self):
        try: self.settings_popup.destroy()
        except: pass
        set_width, set_height = (400, 500)
        self.settings_popup = Toplevel(self.window)
        self.settings_popup.title('Settings')
        self.settings_popup.geometry(f'{set_width}x{set_height}')
        self.settings_popup.resizable(False, False)

        substitution_settings = LabelFrame(self.settings_popup, text='Substitutions')
        other_settings = LabelFrame(self.settings_popup, text='Other settings')

        _frame = Frame(substitution_settings, borderwidth=0)
        _canvas = Canvas(_frame, borderwidth=0)
        _scroll = Scrollbar(_frame, orient='vertical', command=_canvas.yview)
        _frame_inner = Frame(_canvas, borderwidth=0)
        
        def entry_focused(ent, event):
            if ent.get() == 'ignored':
                ent.delete(0, 'end')
            return
        
        def entry_unfocused(ent, char, event):
            text = ent.get().strip()
            if text == '': 
                ent.delete(0, 'end')
                ent.insert(0, 'ignored')
            SUBSTITUTABLES[char] = text
            return

        self._substitution_widgets = dict()
        for idx, (char, subst) in enumerate(SUBSTITUTABLES.items()):
            lbl = Label(_frame_inner, text=char, font=(self._font, 12))
            ent = Entry(_frame_inner, font=(self._font, 12))
            ent.insert(0, subst)
            ent.bind('<FocusIn>', partial(entry_focused, ent))
            ent.bind('<FocusOut>', partial(entry_unfocused, ent, char))
            lbl.grid(row=idx//2, column=(idx%2)*2, padx=2, pady=2, sticky='nsew')
            ent.grid(row=idx//2, column=((idx%2)*2)+1, padx=2, pady=2, sticky='nsew')
            self._substitution_widgets[char] = dict(
                _label=lbl,
                _entry=ent
            )

        denom = { 'win32': 120, 'darwin': 1 }[platform]
        _canvas.configure(yscrollcommand=_scroll.set)
        _canvas.bind('<Configure>', lambda event: _canvas.configure(scrollregion=_canvas.bbox('all')))
        _canvas.bind_all('<MouseWheel>', lambda event: _canvas.yview_scroll(int(-1*(event.delta/denom)), "units"))
        _canvas.create_window((0, 0), window=_frame_inner, anchor='nw')

        self.widgets['chk_autosubstitute'] = Checkbutton(
            other_settings, 
            text='Auto-substitute',
            variable=self._settings['auto_sub']
            )
        self.widgets['lbl_autosubstitute'] = Message(
            other_settings,
            text='Automatically substitute invalid characters according to the application settings as they are entered (recommended for when pasting lots of text, with substitutions active)',
            font=(self._font, 11, 'italic')
        )
        self.widgets['chk_autosubstitute'].grid(row=1, column=0, padx=15, pady=(5, 0), sticky='sw')
        self.widgets['lbl_autosubstitute'].grid(row=2, column=0, padx=15, pady=(0, 5), sticky='new')

        self.widgets['chk_complextokens'] = Checkbutton(
            other_settings,
            text='Use complex tokens',
            variable=self._settings['complex_tokens'],
            command=partial(self.callbacks.toggle_complex, self)
        )
        self.widgets['lbl_complextokens'] = Message(
            other_settings,
            text='Require use of complex tokens, which specify in which octave each note is played (eg. \'A:4-E:3-E:4-A:4\'). Cannot be used with Auto-Substitute',
            font=(self._font, 11, 'italic')
        )
        self.widgets['chk_complextokens'].grid(row=1, column=1, padx=15, pady=(5, 0), sticky='sw')
        self.widgets['lbl_complextokens'].grid(row=2, column=1, padx=15, pady=(0, 5), sticky='new')

        self.widgets['btn_randomisesubstitutions'] = Button(
            other_settings, #_canvas
            text='Randomise all',
            command=partial(self.callbacks.set_substitutions, self, 'randomise')
        )
        self.widgets['btn_randomisesubstitutions'].grid(row=3, column=0, padx=10, ipadx=10, ipady=25, sticky='ns')
        # self.widgets['btn_randomisesubstitutions'].pack(side='left', anchor='s')
        self.widgets['btn_resetsubstitutions'] = Button(
            other_settings, #_canvas
            text='Reset all',
            command=partial(self.callbacks.set_substitutions, self, 'reset')
        )
        self.widgets['btn_resetsubstitutions'].grid(row=3, column=1, padx=10, ipadx=10, ipady=25, sticky='ns')
        # self.widgets['btn_resetsubstitutions'].pack(side='right', anchor='s')
        _frame.pack(fill='both', expand=True)
        _canvas.pack(side='left', fill='both', expand=True)
        _scroll.pack(side='right', fill='y', expand=False)
        substitution_settings.pack(padx=15, pady=5, fill='both', expand=True)
        other_settings.pack(padx=15, pady=5, fill='both', expand=True)

        #TODO: Fix 'ComplexTokens' and 'AutoSub' options, then remove the following lines
        self.widgets['chk_autosubstitute'].configure(state='disabled')
        self.widgets['chk_complextokens'].configure(state='disabled')


        self.settings_popup.mainloop()

    class callbacks:
        def convert(self):
            self.callbacks.data_inputted(self, False)
            data = self.widgets['text_main'][0].get('1.0', 'end')[:-1].split(self.delimiter)

            melody_line = list(map(lambda a: [convert_to_pitch(a[1]), a[0], 1], enumerate(data)))
            nmelody = [melody_line[0]]
            for (pitch, time, duration) in melody_line[1:]:
                if pitch == nmelody[-1][0]:
                    nmelody[-1][2]+=1
                else:
                    nmelody.append([pitch, time, duration])

            mf = MIDIFile(1)
            track, time = 0, 0
            tempo = 120

            mf.addTrackName(track, time, "Sample Track")
            mf.addTempo(track, time, tempo)
            channel, volume = 0, 100

            for (pitch, time, duration) in nmelody:
                mf.addNote(track, channel, pitch, time, duration, volume)

            with open("output.mid", 'wb') as outf:
                mf.writeFile(outf)

        def resize(self, event):
            self._width, self._height = event.width, event.height
        
        def toggle_complex(self):
            if self._settings['complex_tokens'].get() == 1:
                self._settings['auto_sub'].set(0)
                self.widgets['chk_autosubstitute'].configure(state='disabled')
            else:
                self.widgets['chk_autosubstitute'].configure(state='active')
        
        def data_inputted(self, event):
            if self._settings['auto_sub'].get() == 0 and event: return
            self.widgets['text_main'][0].bind('<<TextModified>>', lambda e: None)

            pre_format = self.widgets['text_main'][0].get('1.0', 'end')[:-1].lower()
            pre_format = pre_format.replace('\n', self.delimiter).replace(' ', self.delimiter).split(self.delimiter)
            formatted = list()
            for word in pre_format:
                if word in VALIDNOTES:
                    formatted.append(word)
                else:
                    for char in word:
                        sub = SUBSTITUTABLES[char]
                        if sub == '':
                            if char in VALIDNOTES:
                                formatted.append(char)
                        elif sub != 'ignored':
                            formatted.append(sub)
            formatted = self.delimiter.join(map(str.capitalize, formatted))
            
            self.widgets['text_main'][0].delete('1.0', 'end')
            self.widgets['text_main'][0].insert('1.0', formatted)

            self.widgets['text_main'][0].bind('<<TextModified>>', partial(self.callbacks.data_inputted, self))

        def paste(self, *args):
            clipboard = self.window.clipboard_get()
            clipboard = clipboard.replace("\n", "\\n")

            try:
                start = self.widgets['text_main'][0].index("sel.first")
                end = self.widgets['text_main'][0].index("sel.last")
                self.widgets['text_main'][0].delete(start, end)
            except Exception as e:
                pass
            self.widgets['text_main'][0].insert("insert", clipboard)

        def set_substitutions(self, option):
            for k in SUBSTITUTABLES.keys():
                if option == 'randomise':
                    SUBSTITUTABLES[k] = ranchoice(VALIDNOTES)
                elif option == 'reset':
                    SUBSTITUTABLES[k] = 'ignored'
            for (char, d) in self._substitution_widgets.items():
                d['_entry'].delete(0, 'end')
                d['_entry'].insert(0, SUBSTITUTABLES[char])


def convert_to_pitch(note_name):
    enharm = ENHARMONICS[note_name]
    return ['C','Db','D','Eb','E','F','Gb','G','Ab','A','Bb','B'].index(enharm if enharm else note_name) + 60


if __name__ == "__main__":

    __version__ = 'v0.1'

    VALIDNOTES = ['a', 'a#', 'bb', 'b', 'cb', 'b#', 'c', 'c#', 'db', 'd', 'd#', 'eb', 'e', 'fb', 'e#', 'f', 'f#', 'gb', 'g', 'g#', 'ab']
    SUBSTITUTABLES = defaultdict(str, {
        k: 'ignored' for k in 'hijklmnopqrstuvwxyz0123456789'
    })
    ENHARMONICS = defaultdict(str, {
        'A#': 'Bb', 'Cb': 'B', 'B#': 'C', 'C#': 'Db', 'D#': 'Eb', 'E#': 'F', 'Fb': 'E', 'F#': 'Gb', 'G#': 'Ab'
    })

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
