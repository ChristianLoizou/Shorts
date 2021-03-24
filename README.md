# Shorts
Some smaller projects which don't each deserve their own repository. 

*Freely available under MIT License.*

## Installation and Usage
### Windows
The latest Windows executable version of any project can be found in _.exe_ format at: *{projectname}/latest.exe*.
Eg. *'intervalpractice/latest.exe'*.

### Mac
The latest Darwin (MacOS) application version of any project can be found in _.app_ format at: *{projectname}/latest.app/*.
Eg. *'intervalpractice/latest.app/'*.

*Note:* Darwin applications appear as folders. The entire folder with name ending in *'.app'* must be downloaded to run on MacOS.

### Linux
*Coming soon*

### Source
To compile from source code, you can clone into the git repository, and execute the latest version found at: *{projectname}/main.py*. This will clone the entire repository to your computer, downloading all projects in the repo, so if you only want one, I recommend manually downloading from the project folder (see below).
The commands to clone the whole repo are:

```
git clone git@github.com:ChristianLoizou/Shorts.git
cd shorts/{PROJECT}
python37 main.py
``` 

NOTE: [Python version 3.7+](https://python.org/downloads/) is required to compile from source. You also need [git command line](https://git-scm.com/) to clone from the command line. If you don't want to clone the whole repo, download:
 - *main.py* - Source code file
 - *assets/* - Contains icons / other assets
 - *application_update.py* - Can be left out if you don't need the auto-update feature

 If you plan on leaving out *application_update.py*, check first that the version you are using is capable of running without it. 12toneapp v1.6.1, intervalpractice v1.5 and parallelchecker v1.4.2 are the earliest versions that allow for execution without checking for updates.

Please also note that depending on your PATH environment variable / operating system, `python37`  may be accessed under `python3.7`. Usually `python37` works on Windows, and `python3.7` works for Darwin (MacOS). 
### Requests
Submit a fork if you've improved / added anything to any of the projects and I'll review and merge!
### Credits
- Nils Meier - *testing*
