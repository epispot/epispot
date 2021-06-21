
import sys


def nightly():
    read_setup = open('setup-nightly.py', 'r').readlines()
    setup_no = 0

    for line, _ in enumerate(read_setup):
        if len(list(read_setup[line])) > 12:
            if list(read_setup[line])[4:11] == list('version'):
                setup_no = line
                break
    
    return ''.join(list(read_setup[setup_no])[13:-3])


def stable():
    read_setup = open('setup.py', 'r').readlines()
    setup_no = 0

    for line, _ in enumerate(read_setup):
        if len(list(read_setup[line])) > 12:
            if list(read_setup[line])[4:11] == list('version'):
                setup_no = line
                break
    
    return ''.join(list(read_setup[setup_no])[13:-3])


version_info = None

if sys.argv[1] == 'nightly':
    version_info = nightly()
    print('`setup-nightly.py` version info found: '+version_info)
elif sys.argv[1] == 'stable':
    version_info = stable()
    print('`setup.py` version info found: '+version_info)
else:
    raise ValueError("Exited with 1; no version information found")

read_init = open('epispot/__init__.py', 'r').readlines()
line_no = 0

for line, _ in enumerate(read_init):
    if len(list(read_init[line])) > 8:
        if list(read_init[line])[0:7] == list('version'):
            line_no = line
            break

init_info = read_init[line_no][11:-2]
print('`epispot/__init__.py` version info found: '+init_info)

if version_info == init_info:
    print('Exited with 0; version information matches')
else:
    raise ValueError("Exited with 1; version information doesn't match")
