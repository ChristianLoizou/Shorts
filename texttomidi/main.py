from collections import defaultdict
from functools import partial
from midiutil.MidiFile import MIDIFile
from os import path, sep
from random import choice as ranchoice, randint
from sys import platform
from tkinter import *
from tkinter import font, messagebox
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
            'complex_tokens': IntVar(value=0),
            'conjoin': IntVar(value=1),
            'voices': StringVar(value='1'),
            'randomise_dynamic': IntVar(value=0)
        }
        self.delimiter = ' '

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
        set_width, set_height = (500, 600)
        self.settings_popup = Toplevel(self.window)
        self.settings_popup.title('Settings')
        
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
            SUBSTITUTABLES[char] = text.capitalize()
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

        self.widgets['chk_complextokens'] = Checkbutton(
            other_settings,
            text='Use complex tokens',
            variable=self._settings['complex_tokens'],
            command=partial(self.callbacks.toggle_complex, self)
        )
        self.widgets['chk_complextokens'].grid(row=0, column=1, padx=15, pady=(5, 0), sticky='nesw')

        self.widgets['chk_conjoin'] = Checkbutton(
            other_settings,
            text='Merge adjacent notes',
            variable=self._settings['conjoin']
        )
        self.widgets['chk_conjoin'].grid(row=0, column=0, padx=15, pady=(5, 0), sticky='nesw')

        self.widgets['chk_dynamic'] = Checkbutton(
            other_settings,
            text='Generate random dynamic for each note',
            variable=self._settings['randomise_dynamic']
        )
        self.widgets['chk_dynamic'].grid(row=1, column=0, padx=15, pady=(5, 0), sticky='nesw')

        voice_frame = Frame(other_settings)
        self.widgets['lbl_voices'] = Label(
            voice_frame,
            text='Voices: ',
            font=(self._font, 11)
        )
        self.widgets['lbl_voices'].grid(row=0, column=0, sticky='nesw')

        self.widgets['ent_voices'] = Entry(
            voice_frame, 
            textvariable=self._settings['voices']
        )
        self._settings['voices'].trace('w', partial(self.callbacks.channel_entry, self))

        self.widgets['ent_voices'].grid(row=0, column=1, sticky='nesw')

        voice_frame.grid(row=2, column=0, padx=(15, 2), pady=(5, 0), sticky='nesw')
        

        self.widgets['btn_randomisesubstitutions'] = Button(
            other_settings, # _canvas
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

        #TODO: Put 'reset' and 'randomise' buttons in '_canvas', but not overlapping widgets already in there

        _frame.pack(fill='both', expand=True)
        _canvas.pack(side='left', fill='both', expand=True)
        _scroll.pack(side='right', fill='y', expand=False)
        substitution_settings.pack(padx=15, pady=5, fill='both', expand=True)
        other_settings.pack(padx=15, pady=5, fill='both', expand=True)

        self.settings_popup.mainloop()

    class callbacks:
        def convert(self, *args):
            data = self.widgets['text_main'][0].get('1.0', 'end')
            tokens = data[:-1].split(self.delimiter)
            tokens = list(filter(bool, tokens))

            if self._settings['complex_tokens'].get(): 
                midi_data = self.callbacks.parse_complex_data(self, tokens)
            else: 
                midi_data = self.callbacks.parse_basic_tokens(self, tokens)

            if midi_data:
                create_midi_file(midi_data)


        def resize(self, event):
            self._width, self._height = event.width, event.height
        
        def channel_entry(self, *args):
            data = self._settings['voices'].get()
            def is_int(c):
                try:
                    int(c)
                    return True
                except ValueError:
                    return False
            chars = filter(is_int, list(data))
            ndata = ''.join(chars)
            self._settings['voices'].set(ndata)
        
        def toggle_complex(self):
            if self._settings['complex_tokens'].get() == 1:
                self.widgets['ent_voices'].configure(state='disabled')
                self.widgets['chk_conjoin'].configure(state='disabled')
            else:
                self.widgets['ent_voices'].configure(state='enabled')
                self.widgets['chk_conjoin'].configure(state='enabled')
        
        def parse_complex_data(self, tokens):
            #? COMPLEX TOKEN STRUCTURE: NoteOctave/-:Channel:Duration
            midi_data = defaultdict(list)
            volume = 75

            try:
                for token in tokens:
                    note, channel, duration = token.upper().split(':')
                    channel, duration = int(channel), int(duration)
                    pitch = convert_to_pitch(note, complex=True)
                    time = 0 + sum([n['duration'] for n in midi_data[channel]])
                    if self._settings['randomise_dynamic'].get():
                        volume = randint(MINVOLUME, MAXVOLUME)
                    midi_data[channel].append(
                        dict(pitch=pitch, time=time, duration=duration, volume=volume)
                    )
                return midi_data

            except Exception as e:
                messagebox.showerror(
                    "Could not convert", 
                    'The data entered does not follow the correct token syntax, and could not be converted'
                )
                print(e)
                return None


        def parse_basic_tokens(self, tokens):
            midi_data = dict()
            try:
                nvoices = int(self._settings['voices'].get())
            except ValueError:
                nvoices = 1
            volume = 75

            for vn in range(nvoices):
                midi_data[vn] = list()

            try:
                for idx in range(len(tokens)):
                    channel = idx%nvoices
                    pitch = convert_to_pitch(tokens[idx].capitalize(), complex=False)
                    time = 0 + sum([n['duration'] for n in midi_data[channel]])
                    duration = 1
                    if self._settings['randomise_dynamic'].get():
                        volume = randint(MINVOLUME, MAXVOLUME)

                    midi_data[channel].append(
                        dict(pitch=pitch, time=time, duration=duration, volume=volume)
                    )
                
                nmidi_data = dict()
                if self._settings['conjoin'].get():
                    for channel, line in midi_data.items():
                        nmidi_data[channel] = list()
                        for note in line:
                            try:
                                if nmidi_data[channel][-1]['pitch'] == note['pitch']:
                                    nmidi_data[channel][-1]['duration'] += 1
                                else:
                                    nmidi_data[channel].append(note)
                            except IndexError:
                                nmidi_data[channel].append(note)
                    midi_data = nmidi_data
                return midi_data
            except:
                messagebox.showerror(
                    "Could not convert", 
                    'The data entered is not valid, and could not be converted'
                    )
                return None


        def paste(self, *args):
            clipboard = self.window.clipboard_get()
            clipboard = clipboard.replace("\n", "\\n")

            try:
                start = self.widgets['text_main'][0].index("sel.first")
                end = self.widgets['text_main'][0].index("sel.last")
                self.widgets['text_main'][0].delete(start, end)
                self.widgets['text_main'][0].insert("insert", clipboard)
            except Exception as e:
                pass

        def set_substitutions(self, option):
            for k in SUBSTITUTABLES.keys():
                if option == 'randomise':
                    SUBSTITUTABLES[k] = ranchoice(VALIDNOTES).capitalize()
                elif option == 'reset':
                    SUBSTITUTABLES[k] = 'ignored'
            for (char, d) in self._substitution_widgets.items():
                d['_entry'].delete(0, 'end')
                d['_entry'].insert(0, SUBSTITUTABLES[char])


def convert_to_pitch(note_name, complex=False):
    if note_name in SUBSTITUTABLES.keys():
        note_name = SUBSTITUTABLES[note_name]
    if not complex:
        enharm = ENHARMONICS[note_name]
        return ['C','Db','D','Eb','E','F','Gb','G','Ab','A','Bb','B'].index(enharm if enharm else note_name) + 60
    else:
        #TODO: this \/
        


def create_midi_file(data):
    mf = MIDIFile(1)
    track, time, tempo = 0, 0, 90
    mf.addTrackName(track, time, "Text2Midi")
    mf.addTempo(track, time, tempo)

    for channel, line in data.items():
        for note in line:
            mf.addNote(track, channel, note['pitch'], note['time'], note['duration'], note['volume'])
    
    with open("output.mid", 'wb') as outf:
        mf.writeFile(outf)


if __name__ == "__main__":

    __version__ = 'v0.1'

    MINVOLUME, MAXVOLUME = 30, 100

    VALIDNOTES = ['a', 'a#', 'bb', 'b', 'cb', 'b#', 'c', 'c#', 'db', 'd', 'd#', 'eb', 'e', 'fb', 'e#', 'f', 'f#', 'gb', 'g', 'g#', 'ab']
    SUBSTITUTABLES = defaultdict(str, {
        k: 'ignored' for k in 'hijklmnopqrstuvwxyz0123456789'.upper()
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
