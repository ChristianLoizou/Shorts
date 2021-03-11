import sys
import xml.etree.ElementTree as ElementTree

from itertools import combinations
from tkinter import *
from tkinter.filedialog import askopenfilename as openfilename
from tkinter.ttk import Button, Frame, Label



class Application:
    def __init__(self, width=500, height=500):
        self.width, self.height = width, height
        self.root = Tk()
        self.root.title("Parallel Checker")
        self.root.resizable(False, False)
        self.version = 0.1
        self.setup_window()
    
    def setup_window(self):
        self.mainframe = Frame(self.root, width=self.width, height=self.height)
        self.output_text_variable = StringVar(value='Open a MusicXML file to check it for parallels!')
        out_lbl = Label(self.mainframe, textvariable=self.output_text_variable, width=40)
        load_btn = Button(self.mainframe, text="Load .musicxml file", command=self.load_file, width=40)
        sett_btn = Button(self.mainframe, text="Options", command=self.options_menu, width=40)

        out_lbl.grid(row=0, column=0, columnspan=3, sticky="nsew")
        load_btn.grid(row=1, column=0, sticky="nsew")
        sett_btn.grid(row=2, column=0, sticky="nsew")
        self.mainframe.pack(fill='both', expand=True, padx=15, pady=15)
    
    def run(self):
        self.root.mainloop()
    
    def options_menu(self, _=None):
        print("Options button clicked")
    
    def load_file(self, _=None):
        fn = openfilename(filetypes=[("Uncompressed MusicXML files", '*.musicxml')], title="Load an Uncompressed MusicXML file")
        results = execute_parallel_check(fn)
        self.output_text_variable.set('\n'.join([f"Parallel {i} detected at beat {b} between parts {' and '.join(p)}" for (i, b, p) in results]))
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
            return self.pitch == other.pitch
    
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
    music_dict = dict()
    xml = ElementTree.parse(file_name).getroot()
    
    # for part in xml.part:
    #     music_dict[part['id']] = dict()
    #     for i, measure in enumerate(part.measure):
    #         if i == 0:
    #             key = int(measure.attributes.key.fifths.cdata)
    #         music_dict[part['id']][f"b{measure['number']}"] = list()
    #         for note in measure.note:
    #             music_dict[part['id']][f"b{measure['number']}"].append(Note(note, key))

    for part in xml.findall('part'):
        part_id = part.attrib['id']
        music_dict[part_id] = dict()
        for i, measure in enumerate(part):
            if i == 0:
                key = int(measure.find('attributes').find('key').find('fifths').text)
            music_dict[part_id][f"b{i}"] = list()
            for note in measure.findall('note'):
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
                            octave=note.octave, accidental=note.accidental
                        )
                    )
    return new_data


def check_for_parallels(data):
    try:
        results = list()
        intervals = dict()
        n_parts = len(data)
        length_set = set([len(data[k]) for k in data])
        if len(length_set) != 1:
            raise CustomExceptionTypes.InequalPartLengths("Part lengths must be equal")
        length = length_set.pop()

        part_combinations = list(combinations(list(data.keys()), 2))
        for beat in range(length):
            part_intervals = list()
            for (p1, p2) in part_combinations:
                a, b = data[p1][beat], data[p2][beat]
                part_intervals.append((a, b, a.interval(b)))
            if any([x[2] for x in part_intervals]):
                intervals[beat] = part_intervals
                if beat > 0:
                    last = intervals[beat - 1]
                    for i in range(len(part_combinations)):
                        if part_intervals[i][0] != last[i][0] and part_intervals[i][1] != last[i][1] and part_intervals[i][2] == last[i][2]:
                            results.append((part_intervals[i][2], beat - 1, tuple(part_combinations[i])))                            
        return results
    except CustomExceptionTypes.InequalPartLengths as e:
        print(f"{type(e)}: {e}")

def execute_parallel_check(file_path, _=None):
    data = get_data_dict(file_path)
    data = convert_to_smallest_note_value(data)
    results = check_for_parallels(data)
    return results

if __name__ == "__main__":
    application = Application()
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
