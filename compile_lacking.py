from os import chdir, devnull, listdir, remove, sep, system
from shutil import copyfile as copy
from shutil import rmtree
from subprocess import call
from sys import exit, platform
from time import sleep


def execute_command(command):
    _ = call(command.split(), stdout=open(devnull, 'wb'))


def compile_win(project, version):
    try:
        execute_command('mkdir compilation_files')
    #! TO BE IMPLEMENTED
        rmtree('compilation_files')
        return True
    except Exception as e:
        print(type(e), e)
        return False


def compile_darwin(project, version):
    try:
        execute_command('mkdir compilation_files')
        execute_command(f'mkdir {project}{sep}apps{sep}{version}')
        DEPENDENCIES = ['assets', 'application_update.py']
        execute_command(f'cp {project}{sep}pys{sep}{version}.py compilation_files{sep}{version}.py')
        execute_command(f'cp -r {project}{sep}asset_backups{sep}{version} compilation_files{sep}assets')
        execute_command(f'mv compilation_files{sep}assets{sep}application_update.py compilation_files{sep}application_update.py')
        chdir('compilation_files')
        execute_command(f'py2applet --make-setup {version}.py')
        sleep(.5)
        print("\tWrote 'setup.py'")
        with open('setup.py', 'r') as setup_file:
            setup_lines = setup_file.readlines()
        with open('setup.py', 'w') as setup_file:
            for line in setup_lines:
                if line.startswith('DATA_FILES = '):
                    line = line.replace("[]", repr(DEPENDENCIES))
                setup_file.write(line)
        execute_command('python3.7 setup.py py2app')
        print("\tCompiled application to appfile instance")
        sleep(.5)
        execute_command(f'cp -r dist{sep}{version}.app .{sep}')
        sleep(1)
        for directory in ['build', 'dist', 'assets']: rmtree(directory)
        for file in ['application_update.py', 'setup.py', f'{version}.py']: remove(file)
        print("\tCopied appfile out and cleaned up folders / files")
        execute_command(f'hdiutil create -ov -volname {version} -srcfolder {version}.app {version}.dmg')
        print("\tCompiled appfile to disk-image")
        chdir('..')
        execute_command(f'cp -r compilation_files{sep}{version}.app {project}{sep}apps{sep}{version}{sep}{version}.app')
        execute_command(f'cp compilation_files{sep}{version}.dmg {project}{sep}apps{sep}{version}{sep}{version}.dmg')
        rmtree('compilation_files')
        print("\tSaved appfile and disk-image, and cleaned up compilation files")
        return True
    except Exception as e:
        print(type(e), e, '\n')
        return False

def load_projects():
    with open("VERSION_DATA", 'r') as version_file:
        projects = list(map(lambda l: l.split(':')[0], version_file.readlines()))
    return projects

# Iterate over project folders
project_names = load_projects()
for project in project_names:
    print('\n' + project)
    # Check for incongruence between exes, apps and pys
    exes, apps, pys = (set(listdir(f"{project}{sep}{folder}")) for folder in ('exes', 'apps', 'pys'))
    for s in (exes, apps, pys):
        try: s.remove('.DS_Store')
        except: pass
    exes = set([f.replace('.exe', '') for f in exes])
    pys = set([f.replace('.py', '') for f in pys])
    # Compile incongruences based on platform
    if platform == 'win32': platform_compiled = exes
    elif platform == 'darwin': platform_compiled = apps
    incongruent = sorted([f for f in pys if f not in platform_compiled])
    print(f"Found {len(incongruent)} incongruences to compile...")
    for version in incongruent:
        print(f"\nCompiling '{project} {version}' to {platform}")
        if platform == 'win32': out = compile_win(project, version)
        elif platform == 'darwin': out = compile_darwin(project, version)
        if out: print(f"\nCompilation of '{project} {version}' to {platform} complete...\n\n")
        else:
            print(f"Failed to compile '{project} {version}' to {platform}...\n\n")
            exit(0)
        sleep(1)
