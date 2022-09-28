from os import system

system('python3 prepare_singles.py')
for group in ['A','B','C']:
    system(f'python3 create_dyads.py {group}')
