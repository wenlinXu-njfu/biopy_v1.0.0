import os
os.system(command="sed -i 's/\r//' biopy_v1.0.0/bin/*")
os.system(command="chmod u+x biopy_v1.0.0/bin/*")
os.system(command="python biopy_v1.0.0/bin/batch_rename.py -dir biopy_v1.0.0/bin -old .py")
cur_dir = os.path.dirname(__file__)
for file in os.listdir(cur_dir):
    if os.path.isfile(cur_dir + f'/{file}'):
        os.remove(cur_dir + f'/{file}')
