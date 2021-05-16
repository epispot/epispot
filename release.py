
read_setup = open('setup-nightly.py', 'r').readlines()
setup_no = 0

for line, _ in enumerate(read_setup):
    if len(list(read_setup[line])) > 12:
        if list(read_setup[line])[4:11] == list('version'):
            setup_no = line
            break

version_info = ''.join(list(read_setup[setup_no])[13:-3])
base_version = '.'.join(version_info.split('.')[:-1])
commit_num = int(version_info.split('.')[-1])

write_init = open('setup-nightly.py', 'w')
read_setup[setup_no] = '    version="'+base_version+'.'+str(commit_num + 1)+'",\n'
write_init.writelines(read_setup)

print('setup-nightly.py release info updated')

read_init = open('epispot/__init__.py', 'r').readlines()
line_no = 0

for line, _ in enumerate(read_init):
    if len(list(read_init[line])) > 8:
        if list(read_init[line])[0:7] == list('version'):
            line_no = line
            break

write_init = open('epispot/__init__.py', 'w')
read_init[line_no] = "version = '"+base_version+"."+str(commit_num + 1)+"'\n"
write_init.writelines(read_init)

print('epispot/__init__ release info updated')
