from carding import *
import shutil
from parse import *
import pathlib

root = pathlib.Path(__file__).parents[0]
FULLTEXT = root / 'fulltext'
EXPLAIN = root / 'explain'
OUTPUT = root / 'out.csv'

TOPIC = "馮諼客孟嘗君"

explanatory = load_explanatory(EXPLAIN)
fulltext = load_fulltext(FULLTEXT)

print(fulltext)

width, height = shutil.get_terminal_size()

for _ in range(int(height*0.5)):
    print(" "*width)

fp = open(OUTPUT, mode='a', encoding='utf-8', buffering=1)

for i, (hd, exp) in enumerate(explanatory.items()):
    extra = ''
    jump_flag = False
    exit_flag = False
    ocurs = get_ocur(fulltext, hd)
    idx = 0
    rng = [8,8]

    while(True):
        nont = 1
        for _ in range(height):
            print(" "*width)
        quota = get_text(fulltext, hd, rng, ocurs[idx])

        create_card_view(TOPIC, quota, exp)
        pack = (nont, rng, extra, jump_flag)

        nont, rng, extra, jump_flag, ctnu = process_user_input(*pack)

        if ctnu is None:
            exit_flag = True
            break

        if ctnu:
            break
           

    print(jump_flag)

    if exit_flag:
        break
    if not jump_flag:
        fp.write(f'{TOPIC},{quota[0]},{quota[1]},{quota[2]},{exp},{extra}\n')

fp.close()
