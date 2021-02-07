
read_setup = open('setup.py', 'r').readlines()
version_info = ''.join(list('.'.join(list(read_setup[7].split('.')[:-1])))[13:])
commit_num = int(''.join(list(read_setup[7].split('.')[3])[:-3]))

write_setup = open('setup.py', 'w')
read_setup[7] = '    version="'+version_info+'.'+str(commit_num + 1)+'",\n'
write_setup.writelines(read_setup)

print('setup.py release info updated')

read_init = open('epispot/__init__.py', 'r').readlines()
line_no = 0

for line in range(len(read_init)):
    if list(read_init[line])[0] == '_':
        line_no = line
        break

write_init = open('epispot/__init__.py', 'w')
read_init[line_no] = '__version__ = "'+version_info+'.'+str(commit_num + 1)+'"  # version (v#.#.#)\n'
write_init.writelines(read_init)

print('epispot/__init__ release info updated')
