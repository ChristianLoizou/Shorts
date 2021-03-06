#!usr/bin/env python3
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Button, Checkbutton, LabelFrame, Style
from math import acos, degrees, hypot
from sys import platform
import random
import turtle

class Interval:
    def __init__(self, interval_string, direction):
        self.interval = interval_string
        self.direction = direction
        self.value = self.get_value()
    
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

def generate_exercise(num_intervals=7):
    activated_intervals = get_activated_intervals()
    if activated_intervals == list():
        return
    intervals = random.choices(activated_intervals, k=num_intervals)
    directions = random.choices([-1, 1], k=num_intervals)
    exercise = [Interval(ex, dr) for (ex,dr) in zip(intervals, directions)]
    return exercise

def setup_window():
    global save_btn
    root = Tk()
    root.title("Interval Practice")

    canvas = Canvas(root, width=WIDTH, height=HEIGHT)
    btn_canvas = Canvas(root, width=WIDTH, height=75)
    new_btn = Button(btn_canvas, text="Generate new exercise", command=rerun_application)
    save_btn = Button(btn_canvas, text="Play exercise", command=play_exercise, state="disabled")
    settings_btn = Button(btn_canvas, text="Intervals", command=settings)
    
    canvas.grid(row=0, column=0)
    btn_canvas.grid(row=1, column=0)
    new_btn.grid(row=0, column=0, sticky='nsew')
    save_btn.grid(row=0, column=1, sticky='nsew')
    settings_btn.grid(row=0, column=2, sticky='nsew')
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
    global save_btn
    save_btn.config(state="enabled")

    cx = -(WIDTH-XPAD)//2
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

def play_exercise():
    assert platform != "darwin", "Your operating system does not support playing exercises!"
    return 


def rerun_application():
    exercise = generate_exercise()
    if exercise is not None:
        draw_exercise(exercise, canvas)
    else:
        messagebox.showerror("Could not create exercise", "No intervals have been selected to test. Please select at least one interval in the 'intervals' menu and try again")

def settings():
    settings_styles = Style()
    settings_styles.configure("SettingsLabelframe.TLabelframe.Label", font=("Verdana", 18, "normal"))
    settings_styles.configure("SettingsLabelframe.TLabelframe.Label", foreground='black')

    popup = Toplevel()
    popup.title("Intervals")
    popup.transient(window)
    popup.resizable(False, False)

    interval_frame = LabelFrame(popup, text="Intervals to test", style="SettingsLabelframe.TLabelframe")
    for idx, (setting, value) in enumerate(INTERVALS_ACTIVATED.items()):
        cb = Checkbutton(interval_frame, text=str(Interval(setting, 1)), variable=value, style="SettingsCheckbutton.TCheckbutton")
        cb.grid(row=(idx//2)+1, column=(idx%2)+1, sticky='nsew')
    interval_frame.pack(fill='both', expand=True)
    
    popup.mainloop()

if __name__ == "__main__":

    WIDTH, HEIGHT = (1200, 500)
    XPAD = 50
    MAX_INTERVAL = 8
    MAX_DY = HEIGHT // 4
    TURTLESIZE = (.4, .4)

    INTERVAL_DESCRIPTORS = {
        2: ('nd', ['Minor', 'Major']),
        3: ('rd', ['Minor', 'Major']),
        4: ('th', ['Diminished', 'Perfect', 'Augmented']),
        5: ('th', ['Diminished', 'Perfect', 'Augmented']),
        6: ('th', ['Minor', 'Major']),
        7: ('th', ['Minor', 'Major']),
        8: ('th', ['Perfect'])
    }

    INTERVALS = [f"{t} {a}{b[0]}" for (a,b) in INTERVAL_DESCRIPTORS.items() for t in b[1]]

    window, canvas = setup_window()

    INTERVALS_ACTIVATED = {interval: IntVar(window, value=1) for interval in INTERVALS}

    turt = create_new_turtle(canvas)
    window.mainloop()
