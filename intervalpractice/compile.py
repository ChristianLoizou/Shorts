from shutil import copyfile as copy, rmtree
from os import chdir, listdir, remove, system

PROJECT_NAME = "intervalpractice"

chdir('..')
with open("VERSION_DATA", 'r') as version_data_file:
    version_data = dict(map(lambda l: l.replace("\n", '').split(":"), version_data_file.readlines()))

last_version = version_data[PROJECT_NAME][1:]
curr_version = input(f"Last version number was {last_version!r}\nEnter new version number: ")

with open("VERSION_DATA", 'w') as version_data_file:
    for line in version_data:
        if PROJECT_NAME in line:
            version_data_file.writeline(line.replace(last_version, curr_version))
        else:
            version_data_file.writeline(line)

chdir(PROJECT_NAME)
copy('main.py', f'v{curr_version}.py')
if 'latest.py' in listdir():
    copy('latest.exe', f'exes\\v{last_version}.exe')
system("pyinstaller --onefile -w main.py")
copy('dist\\main.exe', 'latest.exe')
copy('latest.exe', f'exes\\v{curr_version}.exe')
for directory in ["dist", "build", "__pycache__"]:
    rmtree(directory)
remove('main.spec')
