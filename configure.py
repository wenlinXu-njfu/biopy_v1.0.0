import os
path = os.path.dirname(__file__)
os.system(command=f"sed -i 's/\r//' {path}/bin/*")
os.system(command=f"chmod u+x {path}/bin/*")
os.system(command=f"python {path}/bin/batch_rename.py -dir {path}/bin -old .py")
for file in os.listdir(path):
    if os.path.isfile(path + f'/{file}'):
        os.remove(path + f'/{file}')
