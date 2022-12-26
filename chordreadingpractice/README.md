# Chord Reading Practice Application

An application to help you practise sight-reading your chords. Chords are generated (up to four notes per chord), and the user should try to play them in sequence. 

The Python file of the latest release is *'/main.py'.* 

The Windows executable of the latest release is *'/latest_exe/'*. [^1]

The Darwin (MacOS) application of the latest release is *'/latest-darwin/latest.dmg'*. [^2]

For all releases please see 'exes', 'apps' or 'pys' folders.

[^1]:*Note for Windows users: This application requires all the data files located in* <code>latest_exe</code>*. The executable cannot be run unless these files are located in the same folder. The **entire** <code>latest_exe</code> folder must be downloaded for this program to work correctly. You **can** make a shortcut to the executable outside the folder.*

[^2]:<u>Note: Darwin application is currently not available</u>


### Setup

This program reqiures a working intallation of [LilyPond](https://lilypond.org). Make sure the <code>lilypond.exe</code> file (located in the <code>/bin</code> folder) is accessible via your machine's **PATH** (environment variables). 

If you are on Linux / MacOS, I recommend using [HomeBrew](https://brew.sh). The formula for installing LilyPond is <code>brew install lilypond</code>. This should automatically append the LilyPond executable to your **PATH**.
For other download options, see [this page](https://lilypond.org/download.html).

If you are on Windows, you must install the [latest stable version](https://lilypond.org/download.html) of LilyPond, extract the *.zip* to somewhere safe on your machine, (ie. somewhere you won't accidentally move / delete it), then add the complete path to the <code>/bin</code> folder to your path [like this](https://www.architectryan.com/2018/03/17/add-to-the-path-on-windows-10/). 
Eg. If you have intalled *LilyPond version 2.25.0* and put the extracted folder in <code>C:\Users\USERNAME\Documents\\</code>, you will have to add <code>C:\Users\USERNAME\Documents\lilypond-2.25.0\bin\\</code> to your **PATH**.