import os
os.system(command="sed -i 's/\r//' biopy/bin/*")
os.system(command="chmod u+x biopy/bin/*")
os.system(command="python biopy/bin/batch_rename.py -dir biopy/bin -old .py")
cur_dir = os.path.dirname(__file__)
for file in os.listdir(cur_dir):
    if os.path.isfile(cur_dir + f'/{file}'):
        os.remove(cur_dir + f'/{file}')
