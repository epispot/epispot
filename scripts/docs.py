import os

read_setup = open('../setup.py', 'r').readlines()
version_info = ''.join(list('.'.join(list(read_setup[7].split('.')[:-1])))[13:])
commit_num = int(''.join(list(read_setup[7].split('.')[3])[:-3]))

read_setup1 = open('../docs/conf.py', 'r').readlines()
write_setup = open('../docs/conf.py', 'w')
read_setup1[24] = 'release="'+version_info+'.'+str(commit_num + 1)+'"\n'
ws = ''
for x in read_setup1:
    ws += x
write_setup.write(ws)
print('docs/conf.py release info updated')

with os.scandir('../epispot/') as it:
    for entry in it:
        if entry.is_file() and not entry.name == '__init__.py' and not entry.name.endswith('.cpython-38.pyc'):
            rstbase = entry.name.split('.')[0]+''' Module
=====================================================================================
.. automodule:: epispot.'''+entry.name.split('.')[0]+'''
    :members:

'''
            f = open('../docs/'+entry.name.split('.')[0]+'.rst', 'w')
            f.write(rstbase)

print('Docs updated')

os.system('cd docs')
os.system('make html')

print('Updated HTML')
print('Job completed!')
