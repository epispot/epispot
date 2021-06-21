"""
This script is intended to check version information agreement before publishing a package.

The script takes two arguments: 
 (1) Deployment:
     string equal to either 'stable' or 'nightly'--
     This indicates which version information to check (setup.py or setup-nightly.py, respectively).
 (2) Normalized Version Tag:
     The normalized version tag (i.e. the version tag found in epispot's manifest files--without any 'v' prefixes)--
     This is intended as a precaution to ensure that whoever triggered the script is aware of the version 
     that they are deploying.

The script will then run the following routine:
 (1) Store received version information from parameter
 (2) Run a query on the corresponding setup file and obtain version information
 (3) Run a query on epispot's __init__ file and obtain version information
 (4) Check for agreement:
     (a) All three sources of version information agree ==>
         Exit code: 0 (pass)
     (b) One or more sources of version information are not in agreement ==>
         Exit code: 1 (fail)
"""

import sys
received_version_info = sys.argv[2]
print('Received version information obtained: '+received_version_info)


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

if received_version_info == version_info and version_info == init_info:
    print('Exited with 0; version information matches')
else:
    raise ValueError("Exited with 1; version information doesn't match")
