from shutil import copyfile as copy, rmtree
from os import chdir, listdir, remove, system

PROJECT_NAME = "intervalpractice"

chdir('..')
with open("VERSION_DATA", 'r') as version_data_file:
    version_data = dict(map(lambda l: l.replace("\n", '').split(":"), version_data_file.readlines()))

last_version = version_data[PROJECT_NAME]
curr_version = input(f"Last version number was {last_version!r}\nEnter new version number: ").replace('v', '')

with open("VERSION_DATA", 'w') as version_data_file:
    for l in version_data.items():
        if PROJECT_NAME == l[0]:
            version_data_file.write(f"{PROJECT_NAME}:v{curr_version}\n")
        else:
            version_data_file.write(':'.join(l) + "\n")

chdir(PROJECT_NAME)
copy('main.py', f'pys\\v{curr_version}.py')
if 'latest.py' in listdir():
    copy('latest.exe', f'exes\\v{last_version}.exe')
system("pyinstaller --onefile -w main.py")
copy('dist\\main.exe', 'latest.exe')
copy('latest.exe', f'exes\\v{curr_version}.exe')
for directory in ["dist", "build", "__pycache__"]:
    rmtree(directory)
remove('main.spec')
