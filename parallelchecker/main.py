#!usr/bin/env python3
import os
import sys
import xml.etree.ElementTree as ElementTree
from itertools import combinations
from sys import exit
from tkinter import *
from tkinter.filedialog import askopenfilename as openfilename
from tkinter.ttk import Button, Checkbutton, Frame, Label, LabelFrame, Style

from application_update import execute_update


class Application:
    def __init__(self, width=700, height=700):
        self.width, self.height = width, height
        self.root = Tk()
        self.root.config(background=BACKGROUND_COL)
        self.root.title("Parallel Checker")
        self.root.geometry(f"{width}x{height}")
        self.root.resizable(False, False)
        self.root.tk.call('wm', 'iconphoto', self.root._w, PhotoImage(file=f'assets{os.sep}icon.png'))
        self.version = "v1.4"
        self.setup_window()
    
    def setup_window(self):
        self.mainframe = Frame(self.root, width=self.width, height=self.height)
        self.output_text_variable = StringVar(value='Open a MusicXML file to check it for parallels!')
        out_lbl = Label(self.mainframe, textvariable=self.output_text_variable, width=self.width/5)
        load_btn = Button(self.mainframe, text="Load XML/MusicXML file", command=self.load_file, width=self.width/5)
        sett_btn = Button(self.mainframe, text="Options", command=self.options_menu, width=self.width/5)

        out_lbl.grid(row=0, column=0, columnspan=3, sticky="nsew")
        load_btn.grid(row=1, column=0, columnspan=3, sticky="nsew")
        sett_btn.grid(row=2, column=0, columnspan=3, sticky="nsew")
        self.mainframe.place(anchor='c', relx=.5, rely=.5)
    
    def run(self):
        self.root.mainloop()
    
    def options_menu(self):
        settings_styles = Style()
        settings_styles.configure("SettingsLabelframe.TLabelframe.Label", font=("Verdana", 15, "normal"))
        settings_styles.configure("SettingsLabelframe.TLabelframe.Label", foreground='black')

        popup = Toplevel(self.root)
        popup.title("Options")
        popup.resizable(False, False)
        mainframe = Frame(popup)
        int_frame = LabelFrame(mainframe, text="Parallels to detect", style="SettingsLabelframe.TLabelframe")
        other_frame = LabelFrame(mainframe, text="Other options", style="SettingsLabelframe.TLabelframe")
        # int_frame options
        Message(
            int_frame,
            text="Note: these will also detect compound versions of themselves (ie. Compound Perfect 5th)",
            background=BACKGROUND_COL).pack(anchor='w', padx=15, pady=15)
        for i, i_n in enumerate(interval_names):
            cb = Checkbutton(int_frame, text=i_n, variable=interval_variables[i])
            cb.pack(anchor='w', padx=15)
        Button(int_frame, text="Toggle all", command=all_intervals).pack()
        # other_frame options
        Checkbutton(other_frame, text="Reduce data", variable=toggle_reduce_data).pack(anchor='w', padx=15)
        Message(other_frame,
            text="Reducing data will remove all trailing whitespace at the end of a file. " + \
                "Deselect this if there is a point of silence (where all parts are at rest) in your chorale",
            background=BACKGROUND_COL).pack()

        # display all
        int_frame.grid(row=0, column=0, ipadx=15, ipady=15, padx=15, pady=15, sticky="nsew")
        other_frame.grid(row=0, column=1, ipadx=15, ipady=15, padx=15, pady=15, sticky="nsew")        
        mainframe.pack()
        popup.mainloop()
    
    def load_file(self, _=None):
        fn = openfilename(
            filetypes=[
                ("XML files", '*.xml'),
                ("Uncompressed MusicXML files", '*.musicxml')
                ],
            title="Load an XML file")
        self.root.title(f"Parallel Checker - {fn}")
        results = execute_parallel_check(fn)
        results = filter(lambda t: interval_variables[interval_names.index(convert_interval_to_name(t[0]).replace("Compound ", ''))].get()==1, results)
        lines = [
            f"Parallel {convert_interval_to_name(i)} detected in bar {b} between {' and '.join([part_instruments[p_] for p_ in p])}" 
            for (i, b, p) in results
        ]
        if not lines:
            lines = ['No matching parallels found! Did you forget to select an interval in the options menu?']
        self.output_text_variable.set('\n'.join(lines))
        return


class Note:
    def __init__(self, *args, **kwargs):
        if len(args) == 2:
            el, fifths = args
            self.duration = int(el.find('duration').text)
            self.rest = el.find('rest') is not None
            self.key = keys[fifths]
            if not self.rest:
                self.step = el.find('pitch').find('step').text
                self.octave = int(el.find('pitch').find('octave').text)
                try:
                    self.accidental = {
                        'flat-flat': 'bb',
                        'flat': 'b',
                        'natural': '',
                        'sharp': '#',
                        'double_sharp': 'x'
                    }[el.find('accidental').text]
                except:
                    self.accidental = self.key[self.step]
                self.pitch = f"{self.step}{self.accidental}{self.octave}"
            else:
                self.step, self.octave, self.pitch, self.accidental = (None,)*4
        else:
            self.__dict__ = kwargs
            self.enharm = self.get_simplest_enharmonic()
    
    def __repr__(self):
        if self.rest:
            return f"Rest: <duration={self.duration}>"
        else:
            return f"Note: <pitch={self.pitch!r}, accidental={self.accidental!r}, duration={self.duration!r}>"
    
    def __eq__(self, other):
        if self.rest and other.rest:
            return self.duration == other.duration
        else:
            return self.enharm == other.enharm
    
    def get_simplest_enharmonic(self):
        if self.accidental in ('', 'b'):
            return self.pitch
        elif self.accidental == '#':
            return pitches[pitches.index(self.step + str(self.octave)) + 1]
        elif self.accidental == 'bb':
            return pitches[pitches.index(self.step + str(self.octave)) - 2]
        elif self.accidental == 'x':
            return pitches[pitches.index(self.step + str(self.octave)) + 2]
    
    def interval(self, other):
        if self.rest or other.rest:
            return None
        else:
            return abs(pitches.index(self.enharm) - pitches.index(other.enharm))


class CustomExceptionTypes:
    class InequalPartLengths(Exception): pass
    

def get_data_dict(file_name):
    global part_instruments
    music_dict = dict()
    part_instruments = dict()
    # time_sigs = dict()
    # smallest_unit = None
    xml = ElementTree.parse(file_name).getroot()

    for part in xml.findall('part'):
        part_id = part.attrib['id']
        part_instruments[part_id] = xml.find('part-list').find(f"score-part[@id='{part_id}']").find('part-name').text
        music_dict[part_id] = dict()
        for i, measure in enumerate(part):
            if i == 0:
                key = int(measure.find('attributes').find('key').find('fifths').text)
                time = measure.find('attributes').find('time')
                # time_sigs[part_id] = f"{time.find('beats').text}/{time.find('beat-type').text}"
            music_dict[part_id][f"b{i}"] = list()
            for note in measure.findall('note'):
                # if smallest_unit is None and note.find('duration').text == '1':
                #     smallest_unit = note.find('type').text
                music_dict[part_id][f"b{i}"].append(Note(note, key))
    return music_dict

def convert_to_smallest_note_value(data):
    new_data = dict()
    for part, bars in data.items():
        new_data[part] = list()
        for barnum in sorted(list(bars.keys()), key=lambda k: int(k[1:])):
            for note in bars[barnum]:
                for k in range(note.duration):
                    pitch = note.pitch
                    new_data[part].append(
                        Note(pitch=pitch, duration=1,
                            rest=pitch is None, step=note.step,
                            octave=note.octave, accidental=note.accidental,
                            measure=barnum, position_in_note=k,
                            full_note_duration=note.duration-1
                        )
                    )
    return new_data

def check_for_parallels(data):
    try:
        len_set = set(map(len, data.values()))
        if len(len_set) != 1:
            raise CustomExceptionTypes.InequalPartLengths("Parts are not all the same length")
        n_beats = len_set.pop()
        results = list()
        part_combis = list(combinations(data.keys(), 2))
        last_intervals = [(a, b, a.interval(b)) for (a, b) in [(data[i][0], data[j][0]) for (i, j) in part_combis]]
        for beat in range(1, 33):
            new_intervals = [(a, b, a.interval(b)) for (a, b) in [(data[i][beat], data[j][beat]) for (i, j) in part_combis]]
            for pnum in range(len(last_intervals)):
                lna, lnb, li = last_intervals[pnum]
                nna, nnb, ni = new_intervals[pnum]
                if (lna != nna and lnb != nnb and li == ni) and \
                    lna.full_note_duration == lna.position_in_note and \
                    lnb.full_note_duration == lnb.position_in_note and \
                    nna.position_in_note == nnb.position_in_note == 0:
                    if lna.measure == nna.measure:
                        b = str(int(lna.measure[1:]) + 1)
                    else:
                        b = f"{int(lna.measure[1:])+1}-{int(nna.measure[1:])+1}"
                    results.append((li, b, part_combis[pnum]))
            last_intervals = new_intervals

        return results
    except CustomExceptionTypes.InequalPartLengths as e:
        print(f"{type(e)}: {e}")

def reduce_data(data):
    cbeat, parts = int(), list(data.keys())
    while any([data[p][cbeat].rest == False for p in parts]):
        cbeat += 1
    return {k: v[:cbeat] for (k, v) in data.items()}

def convert_interval_to_name(interval):
    if interval > len(interval_names):
        i = interval % 12
        if i == 0: i = -1
        return f"Compound {interval_names[i]}"
    return interval_names[interval]

def execute_parallel_check(file_path, _=None):
    data = get_data_dict(file_path)
    data = convert_to_smallest_note_value(data)
    if toggle_reduce_data.get():
        data = reduce_data(data)
    results = check_for_parallels(data)
    return results

def all_intervals():
    global toggle
    for i in interval_variables:
        i.set(toggle)
    toggle = int(not toggle)

if __name__ == "__main__":
    BACKGROUND_COL = "#eeeeee"
    application = Application()

    if execute_update('parallelchecker', application.version, os.path.basename(__file__)):
        exit(0)

    interval_names = [
        "Perfect Unison", "Minor 2nd",
        "Major 2nd", "Minor 3rd",
        "Major 3rd", "Perfect 4th",
        "Augmented 4th / Diminshed 5th", "Perfect 5th",
        "Minor 6th", "Major 6th", "Minor 7th",
        "Major 7th", "Perfect Octave"
    ]

    toggle = 0
    toggle_reduce_data = IntVar(value=0)
    interval_variables = [IntVar(value=1) for _ in range(len(interval_names))]
    note_names = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
    pitches = [f"{note}{octave}" for octave in range(-1, 10) for note in note_names][:-4] # C-1 - G9
    keys = dict()
    order, nms = "FCGDAEB", "ABCDEFG"
    for k in range(-7, 8):
        if k == 0:
            keys[0] = {p: '' for p in nms}
        else:
            if k < 0:
                acc, od = 'b', order[k:]
            else:
                acc, od = '#', order[:k]
            keys[k] = {p: acc if p in od else '' for p in nms}
    application.run()
