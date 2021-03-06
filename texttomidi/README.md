# Text to Midi

An application to take music in the form of text (ie. strings of note-names) and convert them to midi. Also works with linguistic text, ie. paragraphs from text. Note this is not a clone of [jwktje's 'LangoRhythm'](https://github.com/jwktje/langorhythm). If a letter is not a valid note-name, it is substituted according to pre-defined rules - which can be edited by the user.

The Python file of the latest release is *'/main.py'.* 
The Windows executable of the latest release is *'/latest.exe'*.
The Darwin (MacOS) application of the latest release is *'/latest-darwin/latest.dmg'*.
For all releases please see 'exes', 'apps' or 'pys' folders.


### Help
#### Complex tokens
Complex tokens allow the user to include lots of extra information about the instruments, notes and overall piece in general. The format for a complex token is:

``` NOTE/NOTES:VOICE:DURATION ```
or
``` -:VOICE:DURATION```
or 
``` [TEXT]:VOICE```

A Note is any valid pitch letter (including ones that can be substituted) followed by a valid octave number (0-7).
You can create chords by \'adding\' notes with the '+' symbol. (See below for example).

The Voice is always a number. When listing instruments (see below), the order in which the instruments are listed defines, reversed, which instrument is denoted by which number. For example, were you to include this line at the beginning of the text:

``` INSTRUMENTS: VIOLIN, CELLO, PIANO ```

... then all notes in the first voice (voice 1) would be written to the Piano part, voice 2 to the Cello part and voice 3 to the Violin part. An easy way to think of it is the first instrument is the bottom-most in the system, going through the numbers to the top.

 **Please note** that parts are one-per-stave, meaning an instrument that is usually written across two staves (eg. piano, harp, etc), would need to be included twice in the instrument list to appear across two staves. Clefs are automatically assigned to each stave, based on the first note written to that stave.  

 The Duration is the length of the note in crotchet beats. 1 makes the note a crotchet, .5 a quaver, 2 a minim, and so on.

To create a rest, swap the pitch name for a '-', leaving the Voice and Duration of the rest.

To write some text (eg. a dynamic, expression marking, etc), simply write the text encased in square-brackets ( '[', ']' ) and voice. 

An example of a valid set of tokens:

```
TEMPO: 120
TIMESIG: 3/4
KEYSIG: 3-SHARPS-MINOR
INSTRUMENTS: VIOLIN, CELLO, PIANO

-;3;2 [mf];3 c6;3;1 a5;3;1
-;2;1 [p];2 e4;2;.5 c4;2;.5 a3;2;2
[p];1 e3+a2;1;4

```

Note the optional 'flags' at the beginning of the file, and that both ':' and ';' work to separate token-parts.

**TEMPO**: Sets tempo (crotchet=). Defaults to crotchet = 120.

**TIMESIG**: Sets the time signature of the file.

**KEYSIG**: (*WIP*. Not yet working) Defines the key signature of the file. The format for this flag is:

```
NUMBER-ACCIDENTALS-MODE
```

Some examples are A major -> `3-SHARPS-MAJOR`, C# minor -> `4-SHARPS-MINOR`, Bb minor -> `5-FLATS-MINOR`

**INSTRUMENTS**: Defines the instruments in the file. A valid list of instrument names can be found [here](https://raw.githubusercontent.com/ChristianLoizou/Shorts/master/texttomidi/assets/program_codes.json). Comma separated, and in order of top to bottom of music. Note, you only need the name, not the ID number of the instrument. 


### Settings mutually exclusive to Complex Tokenry

**Merge adjacent**:
    With this setting active, if two notes of equal pitch are written adjacent to each other
    they will be marged into one note of greater length. This allows the user to write
    lines with notes of different length without using complex tokens.
    This setting is automatically disabled when using Complex Tokens.

**Random dynamic per note**:
    If this setting is disabled, every note is set to be played at the same volume (75%).
    Enabling this setting will assign each note a random volume between the minimum and maximum volume 
    (see in-app help menu for these values)
    This setting is automatically disabled when using Complex Tokens.

**Voice per line**:
    Enabling this setting will allow the user to write each part\'s line on a seperate
    line of text. If this setting is disabled, all notes must be written on one line
    and the application will cycle through the voices in order of top-bottom.
    This setting is automatically disabled when using Complex Tokens.

**Voices**:
    This setting determines how many parts will be written in the MIDI file. If you have
    the \'voice per line\' setting enabled, this is also the number of lines that will be
    used when creating the MIDI file
    This setting is automatically disabled when using Complex Tokens.

**Tempo**:
    This setting sets the tempo of the MIDI. Default tempo is 120.
    This setting is automatically disabled when using Complex Tokens.