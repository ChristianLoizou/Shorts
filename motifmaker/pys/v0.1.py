import random, pyperclip
from functools import partial
from os import path
from tkinter import *
from tkinter.ttk import Button, Entry, Label, LabelFrame, Menubutton, OptionMenu, Style


MODES = {
        'major': [0, 2, 4, 5, 7, 9, 11],
        'minor': [0, 2, 3, 5, 7, 8, 11],
        'octatonic_tone': [0, 2, 3, 5, 6, 8, 9, 11],
        'octatonic_semi': [0, 1, 3, 4, 6, 7, 9, 10]
    }

SCALES = {
        'sharps': ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'],
        'flats': ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
    }

class Application(Tk):
    def __init__(self, version, *args, **kwargs):
        super(Application, self).__init__(*args, **kwargs)
        self.version = version
        self.title(f"MotifMaker v{self.version}")
        self.resizable(False, False)
        self.validate_entry = self.register(validate_entry)
        self.SETTINGS = {
            'accidental_type': StringVar(self, 'sharps'),
            'motif_length': IntVar(self, 8),
            'key': StringVar(self, 'C'),
            'max_repetitions': IntVar(self, 1),
            'mode': StringVar(self, 'octatonic_tone'),
            'num_voices': StringVar(self, '4')
        }
        self.add_widgets()
    
    def add_widgets(self):
        self.menu = Menu(self)
        self.config(menu=self.menu)
        self.filemenu = Menu(self.menu)
        self.filemenu.add_command(label="Settings", command=self.settings_popup)
        self.filemenu.add_command(label="Information", command=self.information_popup)
        self.filemenu.add_command(label="Exit", command=self.on_exit)
        self.exportmenu = Menu(self.menu)
        self.exportmenu.add_command(label='Export to TXT', command=lambda: self.export('txt'))
        self.exportmenu.add_command(label='Export to MIDI', command=lambda: self.export('midi'))
        self.exportmenu.add_command(label='Export to MXL', command=lambda: self.export('mxml'))
        self.menu.add_cascade(menu=self.filemenu, label='File')
        self.menu.add_cascade(menu=self.exportmenu, label='Export')
        
        self.mainframe = Frame(self, bg='#eeeeee')
        self.lblframe_outputframe = LabelFrame(self.mainframe, text='Output')
        self.text_output = Text(self.lblframe_outputframe, state=DISABLED)
        self.btn_run = Button(self.mainframe, text='Generate sequence', command=self.execute)
        self.btn_copy = Button(self.mainframe, text='Copy output', command=self.copy_output)
        
        self.text_output.pack(expand=True, fill='both', padx=15, pady=15)
        self.lblframe_outputframe.grid(row=0, column=0, rowspan=3, columnspan=4, padx=15, pady=15)
        self.btn_run.grid(row=4, column=1, pady=25)
        self.btn_copy.grid(row=4, column=2, pady=25)
        
        self.mainframe.pack(anchor='center')
    
    def settings_popup(self):
        self.settings_window = Toplevel()
        self.settings_window.title("Settings")
        self.settings_window.resizable(False, False)
        self.settings_window.config(bg='#eeeeee')
        
        self.settings_frames = {
            'motif_length': LabelFrame(self.settings_window, text='Motif length'),
            'num_voices': LabelFrame(self.settings_window, text='Number of voices'),
            'accidental_type': LabelFrame(self.settings_window, text='Accidental type'),
            'key': LabelFrame(self.settings_window, text='Key')
        }
        
        self.settings_widgets = {
            'motif_length_text': Entry(
                self.settings_frames['motif_length'],
                textvariable=self.SETTINGS['motif_length'],
                validate='all',
                validatecommand=(self.validate_entry, 'motif_length', '%P', '%V', '1'),
                width=2
            ),
            'motif_length_lbl': Label(
                self.settings_frames['motif_length'], 
                text='The length of the generated motif',
                font=(None, 11)
            ),
            'num_voices_text': Entry(
                self.settings_frames['num_voices'],
                textvariable=self.SETTINGS['num_voices'],
                validate='all',
                validatecommand=(self.validate_entry, 'num_voices', '%P', '%V', '4'),
                width=2
            ),
            'num_voices_lbl': Label(
                self.settings_frames['num_voices'], 
                text='The number of voices per line in the motif, or a range. Eg: 4-5',
                font=(None, 11)
            ),
            'accidental_type_menu': Menubutton(
                self.settings_frames['accidental_type'],
                text=f"{self.SETTINGS['accidental_type'].get().capitalize()}"
            ),
            'accidental_types_lbl': Label(
                self.settings_frames['accidental_type'], 
                text='The type of accidental used',
                font=(None, 11)
            ),
            'key_menu': Menubutton(
                self.settings_frames['key'],
                text=self.SETTINGS['key'].get()
            ),
            'key_lbl': Label(
                self.settings_frames['key'], 
                text='The key in which the motif should be generated',
                font=(None, 11)
            )
        }

        accidental_types_menu = Menu(self.settings_widgets['accidental_type_menu'], tearoff=False)
        for label in ('Sharps (#)', 'Flats (b)'):
            value = label.split()[0].lower()
            accidental_types_menu.add_radiobutton(
                label=label, 
                value=value, 
                variable=self.SETTINGS['accidental_type'],
                command=partial(self.change_setting, 'accidental_type', value)
            )
        
        key_menu = Menu(self.settings_widgets['key_menu'], tearoff=False)
        for label in SCALES['sharps']:
            key_menu.add_radiobutton(
                label=label, 
                value=label,
                variable=self.SETTINGS['key'],
                command=partial(self.change_setting, 'key', label)
            )
        
        self.settings_widgets['key_menu']['menu'] = key_menu
        self.settings_widgets['accidental_type_menu']['menu'] = accidental_types_menu
        
        for setting in self.settings_widgets.values():
            setting.pack(expand=True, fill='both')
        for fn, frame in enumerate(self.settings_frames.values()):
            frame.grid(row=fn, rowspan=1, column=0, columnspan=3, padx=10, pady=10, sticky='w')
        
        self.settings_window.mainloop()
        self.settings_window.grab_set()
        
    
    def change_setting(self, setting, value):
        self.SETTINGS[setting].set(value)
        if setting == 'accidental_type':
            acc_scale = SCALES[value]
            self.settings_widgets['accidental_type_menu'].configure(text=value.capitalize())
            key_menu = Menu(self.settings_widgets['key_menu'], tearoff=False)
            for label in acc_scale:
                key_menu.add_radiobutton(
                    label=label, 
                    value=label,
                    variable=self.SETTINGS['key'],
                    command=partial(self.change_setting, 'key', label)
                )
            self.settings_widgets['key_menu']['menu'] = key_menu
            enharm_equiv = get_enharmonic_equivalent(self.SETTINGS['key'].get())
            self.SETTINGS['key'].set(enharm_equiv)
            self.settings_widgets['key_menu'].configure(text=enharm_equiv)
            NOTES = SCALES[self.SETTINGS['accidental_type'].get()]
        elif setting == 'key':
            self.settings_widgets['key_menu'].configure(text=value)
        return
    
    def information_popup(self):
        pass
    
    def on_exit(self):        
        self.destroy()
        self.quit()
        
    def execute(self):
        
        generated_data = list() 
        key = self.SETTINGS['key'].get()
        max_repetitions = self.SETTINGS['max_repetitions'].get()
        mode = self.SETTINGS['mode'].get()
        num_voices = self.SETTINGS['num_voices'].get()
        
        for _ in range(self.SETTINGS['motif_length'].get()):
            vn = get_num_voices(num_voices)
            chord = generate_chord(vn, MODES[mode], max_repetitions)
            applied = apply_chord(chord, key)
            generated_data.append('\t'.join(applied.values()))
            
        self.text_output.config(state=NORMAL)
        self.text_output.delete(1.0, END)
        self.text_output.insert(END, '\n'.join(generated_data))
        self.text_output.config(state=DISABLED)
    
    def export(self, output_type):
        print(f"exporting as {output_type!r}")
    
    def copy_output(self):
        pyperclip.copy(self.text_output.get('1.0', END))
    

def get_num_voices(vs):
    l = vs.split('-')
    if len(l) > 1: return random.randint(*sorted(list(map(int,l))))
    else: return int(l[0])

def get_enharmonic_equivalent(note):
    enharms = {'A': 'B', 'B': 'C', 'C': 'D', 'D': 'E', 'E': 'F', 'F': 'G', 'G': 'A'}
    return enharms[note[:-1]]+'b' if '#' in note else {v: k for (k,v) in enharms.items()}[note[:-1]]+'#' if 'b' in note else note

def validate_entry(*args, **kwargs):
    global app
    sett_name, after, reason, default = args
    if type(app.SETTINGS[sett_name]) is IntVar:
        if reason == 'focusout' and after == '': 
            app.SETTINGS[sett_name].set(int(default))
            return True
        return after.isdigit() or after == ''
    elif sett_name == 'num_voices':
        return all(map(str.isdigit, [e for e in after.split('-') if e]))
    else: return True

def generate_chord(voices, mode, max_repetitions):
    chord = dict()
    for vn in range(voices):
        nv = random.choice(mode)
        while list(chord.values()).count(nv) > max_repetitions:
            nv = random.choice(mode)
        chord[vn+1] = nv
    return chord
    
def apply_chord(chord, key):
    ss = NOTES.index(key)
    scale = NOTES[ss:] + NOTES[:ss]
    return {k: scale[v] for (k,v) in chord.items()}



if __name__ == '__main__':
    
    __version__ = '0.1'

    try:
        from application_update import execute_update
        if execute_update('motifmaker', __version__, path.basename(__file__)):
            exit()

    except ModuleNotFoundError:
        pass

    MAX_REPETITION = 1
    MODE = MODES['octatonic_tone']
    NOTES = SCALES['sharps']
    
    app = Application(__version__)
    app.after(500, app.focus_force)
    app.mainloop()