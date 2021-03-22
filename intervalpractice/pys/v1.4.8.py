#!usr/bin/env python3
from application_update import execute_update
from math import acos, degrees, hypot
from sys import platform, exit
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Button, Checkbutton, LabelFrame, OptionMenu, Spinbox, Style
import os
import random
import turtle

if platform == "win32":
    from winsound import Beep as playtone
    from time import sleep
    import threading

class Interval:
    def __init__(self, interval_string, direction):
        self.interval = interval_string
        self.direction = direction
        self.value = self.get_value()
        self.semitones = SEMITONES[self.interval] * self.direction
    
    def __str__(self):
        return self.interval.replace("8th", "Octave")
    
    def __repr__(self):
        return self.interval.replace("8th", "Octave")
    
    def get_value(self):
        vs = list()
        for k in self.interval:
            try:
                vs.append(int(k))
            except ValueError:
                pass 
        return int(''.join(map(str, vs))) * self.direction

    def get_dy(self):
        return self.value * MAX_DY // MAX_INTERVAL

def get_activated_intervals():
    return [ interval for (interval, value) in INTERVALS_ACTIVATED.items() if value.get() == 1 ]

def generate_exercise():
    activated_intervals = get_activated_intervals()
    if activated_intervals == list():
        return
    num_intervals = int(EXERCISE_LENGTH.get())
    intervals = list()
    for i in range(num_intervals):
        c = random.choice(activated_intervals)
        try:
            while (intervals[i-1] == c or (ALLOW_REPETITIONS.get() == 0 and c in intervals)) and len(activated_intervals) > 1:
                c = random.choice(activated_intervals)
            intervals.append(c)
        except:
            intervals.append(c)
            

    directions = random.choices([-1, 1], k=num_intervals)
    exercise = [Interval(ex, dr) for (ex,dr) in zip(intervals, directions)]
    return exercise

def setup_window():
    global play_btn
    root = Tk()
    root.title("Interval Practice")
    root.resizable(False, False)
    root.tk.call('wm', 'iconphoto', root._w, PhotoImage(file=f'assets{os.sep}icon.png'))
    root.after(500, root.focus_force)

    canvas = Canvas(root, width=WIDTH, height=HEIGHT)
    btn_canvas = Canvas(root, width=WIDTH, height=75)
    new_btn = Button(btn_canvas, text="Generate new exercise", command=rerun_application)
    play_btn = Button(btn_canvas, text="Play exercise", command=play_exercise, state="disabled")
    settings_btn = Button(btn_canvas, text="Settings", command=settings)
    play_home_tone_btn = Button(btn_canvas, text="Play starting note", command=play_home_tone)
    
    canvas.grid(row=0, column=0)
    btn_canvas.grid(row=1, column=0)
    new_btn.grid(row=0, column=0, sticky='nsew')
    play_btn.grid(row=0, column=1, sticky='nsew')
    play_home_tone_btn.grid(row=0, column=2, sticky='nsew')
    settings_btn.grid(row=0, column=3, sticky='nsew')

    return root, canvas

def create_new_turtle(canvas):
    turt = turtle.RawTurtle(canvas)
    turt.speed(10)
    turt.penup()
    turt.shape("circle")
    turt.hideturtle()
    turt.turtlesize(*TURTLESIZE)
    for _ in range(2):
        turt.penup()
        turt.pendown()
    return turt

def reset_turtle(turt, x=None, y=None):
    canvas.delete("all")
    turt.speed(10)
    turt.setposition(x if x else 0, y if y else 0)

def draw_exercise(exercise, canvas):
    global play_btn
    play_btn.config(state="enabled")

    ox = -(WIDTH-XPAD)//2
    cx = ox
    dx = (WIDTH - (XPAD)) // (len(exercise)*2)
    reset_turtle(turt, cx)
    turt.stamp()
    for interval in exercise:
        nx, ny = cx + dx, interval.get_dy()
        lx, cx = cx, nx + dx
        txtangle = degrees(acos(dx/hypot(dx, ny))) * (ny/abs(ny))
        _ = canvas.create_text(lx + (dx//2), -ny//2, text=str(interval), angle=txtangle)

        for k, pos in enumerate([(nx, ny), (cx, 0)]):
            if k: turt.pendown()
            else: turt.penup()
            turt.setposition(*pos)
            turt.stamp()
    turt.setpos(ox, 0)

def play_exercise():
    if platform != "win32":
        messagebox.showerror("Cannot play back exercise", "Your operating system does not support playback")
        return
    notes_to_play, home_idx = [HOME_NOTE], PITCHES.index(HOME_NOTE) 

    for interval in exercise:
        new_note = PITCHES[home_idx + interval.semitones] # providing intervals cannot go out of range
        notes_to_play.append(new_note)
        notes_to_play.append(HOME_NOTE)
    
    freqs_to_play = [FREQUENCY_DICT[p] for p in notes_to_play]
    play_thread = threading.Thread(target=play_notes, args=(freqs_to_play,), daemon=True)
    play_thread.start()


def play_home_tone():
    if platform != "win32":
        messagebox.showerror("Cannot play back exercise", "Your operating system does not support playback")
        return
    play_thread = threading.Thread(target=playtone, args=(FREQUENCY_DICT[HOME_NOTE], TONE_DURATION), daemon=True)
    play_thread.start()

def play_notes(notes):
    pause = [.6, .2, .005][int(PLAYBACK_SPEED.get())-1]
    for freq in notes:
        playtone(freq, TONE_DURATION)
        sleep(pause)

def rerun_application():
    global exercise
    exercise = generate_exercise()
    if exercise is not None:
        draw_exercise(exercise, canvas)
    else:
        messagebox.showerror("Could not create exercise", "No intervals have been selected to test. Please select at least one interval in the 'intervals' menu and try again")

def update_starting_note(_=None):
    global HOME_NOTE, HOME_NOTE_VARIABLE
    HOME_NOTE = f"{HOME_NOTE_VARIABLE.get()}5"


def settings():
    settings_styles = Style()
    settings_styles.configure("SettingsLabelframe.TLabelframe.Label", font=("Verdana", 18, "normal"))
    settings_styles.configure("SettingsLabelframe.TLabelframe.Label", foreground='black')

    popup = Toplevel()
    popup.title("Settings")
    popup.transient(window)
    popup.resizable(False, False)

    interval_frame = LabelFrame(popup, text="Intervals to test", style="SettingsLabelframe.TLabelframe")
    for idx, (setting, value) in enumerate(INTERVALS_ACTIVATED.items()):
        cb = Checkbutton(interval_frame, text=str(Interval(setting, 1)), variable=value, style="SettingsCheckbutton.TCheckbutton")
        cb.grid(row=(idx//2)+1, column=(idx%2)+1, sticky='nsew')
    interval_frame.pack(fill='both', expand=True, padx=15, pady=15, ipadx=5, ipady=5)

    other_frame = LabelFrame(popup, text="Other settings", style="SettingsLabelframe.TLabelframe")
    homenote_lbl = Label(other_frame, text="Starting note: ")
    homenote_om = OptionMenu(other_frame, HOME_NOTE_VARIABLE, *NOTE_NAMES, command=update_starting_note)
    length_lbl = Label(other_frame, text="Exercise length: ")
    length_sb = Spinbox(other_frame, from_=3, to=10, textvariable=EXERCISE_LENGTH, state="readonly", width=5)
    playbackspeed_lbl = Label(other_frame, text="Playback speed: ")
    playbackspeed_sb = Spinbox(other_frame, from_=1, to=3, textvariable=PLAYBACK_SPEED, state="readonly", width=5)
    allowrepetitions_cb = Checkbutton(other_frame, text="Allow repetitions", variable=ALLOW_REPETITIONS, style="SettingsCheckbutton.TCheckbutton")
    

    homenote_lbl.grid(row=0, column=0)
    homenote_om.grid(row=0, column=1)
    length_lbl.grid(row=1, column=0)
    length_sb.grid(row=1, column=1)
    playbackspeed_lbl.grid(row=2, column=0)
    playbackspeed_sb.grid(row=2, column=1)
    allowrepetitions_cb.grid(row=3, column=0, columnspan=2, sticky='w', padx=5)
    other_frame.pack(fill='both', expand=True, padx=15, pady=15, ipadx=5, ipady=5)
    
    popup.mainloop()

if __name__ == "__main__":

    __version__ = "v1.4.8"

    if execute_update('intervalpractice', __version__, os.path.basename(__file__)):
        exit(0)

    WIDTH, HEIGHT = (1200, 500)
    XPAD = 50
    MAX_INTERVAL = 8
    MAX_DY = HEIGHT // 4
    TURTLESIZE = (.4, .4)

    HOME_NOTE = "C5"
    TONE_DURATION = 750

    MAX_EXERSISE_LENGTH = 10
    MIN_EXERSISE_LENGTH = 3

    INTERVAL_DESCRIPTORS = {
        2: ('nd', ['Minor', 'Major']),
        3: ('rd', ['Minor', 'Major']),
        4: ('th', ['Perfect',]),
        5: ('th', ['Diminished', 'Perfect']),
        6: ('th', ['Minor', 'Major']),
        7: ('th', ['Minor', 'Major']),
        8: ('th', ['Perfect'])
    }

    INTERVALS = [f"{t} {a}{b[0]}" for (a,b) in INTERVAL_DESCRIPTORS.items() for t in b[1]]
    SEMITONES = {INTERVALS[k]:k+1 for k in range(len(INTERVALS))}

    start_freq, octaves = 261.63, 3
    NOTE_NAMES = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
    PITCHES = [f"{NOTE_NAMES[i%len(NOTE_NAMES)]}{(i//len(NOTE_NAMES))+4}" for i in range((len(NOTE_NAMES)*octaves)+1)]
    FREQUENCY_DICT = dict(zip(PITCHES, [int(start_freq*(2**(i/12))) for i in range(len(PITCHES))]))

    window, canvas = setup_window()

    HOME_NOTE_VARIABLE = StringVar(value="C")
    EXERCISE_LENGTH = StringVar(value="7")
    PLAYBACK_SPEED = StringVar(value="1")
    ALLOW_REPETITIONS = IntVar(value=0)
    INTERVALS_ACTIVATED = {interval: IntVar(window, value=1) for interval in INTERVALS}

    turt = create_new_turtle(canvas)
    window.mainloop()
