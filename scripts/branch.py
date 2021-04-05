import os
import shutil
from glob import glob

for fname in os.listdir('./docs/epispot/'):
    os.rename('./docs/epispot/'+fname, './docs/'+fname)

for dname in glob("./*/"):
    if dname == 'docs' or dname == 'scripts':
        continue
    
    shutil.rmtree(dname)

for fname in os.path.abspath('.'):
    if fname == 'scripts/branch.py' or fname.find('docs') != -1:
        continue

    os.remove(fname)