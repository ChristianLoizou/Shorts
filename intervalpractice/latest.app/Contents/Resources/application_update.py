import urllib
from os import remove as deletefile
from sys import platform
from tkinter import *
from tkinter import messagebox

import requests
from bs4 import BeautifulSoup

UPDATE_URL = "https://github.com/ChristianLoizou/Shorts/blob/master/VERSION_DATA"
fileexts = {
    'win32': '.exe',
    'darwin': '.app'
}

def retrieve_current_version(application_name):
    source = requests.get(UPDATE_URL).text
    soup = BeautifulSoup(source, 'lxml')
    lines = list(soup.find_all('td', class_='blob-code blob-code-inner js-file-line'))
    line = [line for line in lines if application_name in str(line)][0]
    version = str(line).split('>')[1].split('<')[0].split(":")[1]
    return version

def prompt_update(cv):
    hidden = Tk()
    hidden.withdraw()
    ans = messagebox.askyesno("Update available", f"A new update ({cv}) is available for this application. Would you like to install it?")
    hidden.destroy()
    return ans

def update_application(application, new_version, filename):
    try:
        if platform == 'win32':
            LATEST_RELEASE_URL = f"https://raw.githubusercontent.com/ChristianLoizou/Shorts/master/{application}/latest.{fileexts['win32']}"
            DOWNLOAD_NAME = f"{application}-{new_version}.{fileexts['win32']}"
        elif platform == 'darwin':
            LATEST_RELEASE_URL = f"https://raw.githubusercontent.com/ChristianLoizou/Shorts/master/{application}/main.{fileexts['darwin']}"
            DOWNLOAD_NAME = f"{application}-{new_version}.{fileexts['darwin']}"
        req = requests.get(LATEST_RELEASE_URL, allow_redirects=True)
        with open(DOWNLOAD_NAME, 'wb') as f:
            f.write(req.content)

    except Exception as e:
        hidden = Tk()
        hidden.withdraw()
        ans = messagebox.showerror("Update failed", f"Could not install update. Please install the latest version from GitHub manually at {LATEST_RELEASE_URL!r}")
        hidden.destroy()

def execute_update(application_name, file_version, file_name):
    curr_version = retrieve_current_version(application_name)
    if file_version != curr_version and prompt_update(curr_version):
        update_application(application_name, curr_version, file_name)
        return True
    return False
