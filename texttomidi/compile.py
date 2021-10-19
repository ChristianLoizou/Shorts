from os import chdir, listdir, makedirs, path, remove, sep, system
from shutil import rmtree
from sys import platform
from time import sleep

PROJECT_NAME = "texttomidi"

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
    if not path.exists(f'asset_backups{sep}v{curr_version}{sep}'):
        makedirs(f'asset_backups{sep}v{curr_version}{sep}')
    system(f'xcopy /e /i assets asset_backups{sep}v{curr_version}{sep}assets{sep}')
    system(f'copy application_update.py asset_backups{sep}v{curr_version}{sep}application_update.py')
    system(f'copy main.py pys{sep}v{curr_version}.py')
    if 'latest.py' in listdir():
        system(f'copy latest.exe exes{sep}v{last_version}.exe')
    system("pyinstaller --onefile -w main.py")
    system(f'copy dist{sep}main.exe latest.exe')
    system(f'copy latest.exe exes{sep}v{curr_version}.exe')
    
    for directory in ["dist", "build"]:
        rmtree(directory)
    remove('main.spec')
elif platform == 'darwin':
    system(f'cp -r assets asset_backups{sep}v{curr_version}{sep}assets')
    system(f'cp application_update.py asset_backups{sep}v{curr_version}{sep}application_update.py')
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
    system(f'mkdir apps{sep}v{curr_version}')
    system(f'cp -r dist{sep}main.app{sep} latest-darwin{sep}latest.app{sep}')
    system(f'cp -r dist{sep}main.app{sep} apps{sep}v{curr_version}{sep}v{curr_version}.app{sep}')
    system(f'hdiutil create -ov -volname latest -srcfolder latest-darwin{sep}latest.app latest-darwin{sep}latest.dmg')
    system(f'cp -r latest-darwin{sep}latest.dmg apps{sep}v{curr_version}{sep}v{curr_version}.dmg')
    for directory in ['dist', 'build']:
        rmtree(directory)
    remove('setup.py')
