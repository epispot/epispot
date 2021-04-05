import os
import shutil
from glob import glob

for fname in os.listdir('./docs/epispot/'):
    os.rename('./docs/epispot/'+fname, './docs/'+fname)
