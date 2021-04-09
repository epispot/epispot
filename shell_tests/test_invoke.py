import os

for file in os.listdir("."):
    if file.endswith(".sh"):
        os.system('chmod u+x '+os.path.join("./", file))  # give file run permissions
        os.system(os.path.join("./", file))  # execute test
