from os import chdir, listdir, remove, system
from shutil import copyfile as copy
from shutil import rmtree
from sys import platform
from time import sleep

PROJECT_NAME = "parallelchecker"

print("\nHave you updated the version number in 'main.py'?\n\n")

chdir('..')
with open("VERSION_DATA", 'r') as version_data_file:
    version_data = dict(map(lambda l: l.replace(
        "\n", '').split(":"), version_data_file.readlines()))

last_version = version_data[PROJECT_NAME]
curr_version = input(
    f"Last version number was {last_version!r}\nEnter new version number: ").replace('v', '')

with open("VERSION_DATA", 'w') as version_data_file:
    for l in version_data.items():
        if PROJECT_NAME == l[0]:
            version_data_file.write(f"{PROJECT_NAME}:v{curr_version}\n")
        else:
            version_data_file.write(':'.join(l) + "\n")

chdir(PROJECT_NAME)
if platform == 'win32':
    copy('assets', f'asset_backups\\v{curr_version}')
    copy('main.py', f'pys\\v{curr_version}.py')
    if 'latest.py' in listdir():
        copy('latest.exe', f'exes\\v{last_version}.exe')
    system("pyinstaller --onefile -w main.py")
    copy('dist\\main.exe', 'latest.exe')
    copy('latest.exe', f'exes\\v{curr_version}.exe')
    for directory in ["dist", "build"]:
        rmtree(directory)
    remove('main.spec')
elif platform == 'darwin':
    system(f'cp -r assets asset_backups/v{curr_version}')
    DEPENDENCIES = ['assets', 'application_update.py']
    system('py2applet --make-setup main.py')
    with open('setup.py', 'r') as setup_file:
        setup_lines = setup_file.readlines()
    with open('setup.py', 'w') as setup_file:
        for line in setup_lines:
            if line.startswith('DATA_FILES = '):
                line = line.replace("[]", repr(DEPENDENCIES))
            setup_file.write(line)
    system('python3.7 setup.py py2app')
    sleep(.5)
    system('mkdir latest-darwin')
    system(f'mkdir apps/v{curr_version}')
    system('cp -r dist/main.app/ latest-darwin/latest.app/')
    system(f'cp -r dist/main.app/ apps/v{curr_version}/v{curr_version}.app/')
    system('hdiutil create -ov -volname latest -srcfolder latest-darwin/latest.app latest-darwin/latest.dmg')
    system(f'cp -r latest-darwin/latest.dmg apps/v{curr_version}/v{curr_version}.dmg')
    for directory in ['dist', 'build']:
        rmtree(directory)
    remove('setup.py')

