from carding import *
from parse import *
import pathlib
import shutil
import hashlib

root = pathlib.Path(__file__).parents[0]
FULLTEXT = root / 'fulltext'
EXPLAIN = root / 'explain.md'
OUTPUT = root / 'out.csv'
DATA =  root / 'data' / 'processed_hashes'

TOPIC = "勸和論"

check = True

explanatory = load_explanatory(EXPLAIN)
fulltext = load_fulltext(FULLTEXT)
DATA.parents[0].mkdir(parents=True, exist_ok=True)
if not DATA.exists():
    open(DATA, mode='w').close()
hash_file = open(DATA, mode='r+', encoding='utf-8', buffering=1)
hash_data = hash_file.read().splitlines()

if check:
    failed_lines = []
    for exp, _ in explanatory:
        if exp not in fulltext:
            failed_lines.append(f'FAILED, {exp}')
    if len(failed_lines) > 0:
        printScreen(failed_lines)
        input()

fp = open(OUTPUT, mode='a', encoding='utf-8', buffering=1)

for i, (hd, exp) in enumerate(explanatory):
    ocurs = get_ocur(fulltext, hd)
    if getHash(exp) in hash_data:
        print(f'{exp} exists, skipping')
        continue

    # ?
    info = {}
    info['fulltext'] = fulltext
    info['hd'] = hd
    info['rng'] = [8,8]
    info['ocur'] = ocurs[0]
    info['idx'] = 0
    info['extra'] = ''
    status = Status.ADJUST 

    while(status == Status.ADJUST):
        info['position'] = fulltext.index(hd, info['ocur'])
        idx = info['idx'] % len(ocurs)
        quota = get_text(fulltext, hd, info['rng'], ocurs[idx])

        countdown = f'({i}/{len(explanatory)})'

        create_card_view(TOPIC + countdown, quota, exp)

        status, info = process_input(**info)


    if status == Status.EXIT:
        break
    if status == Status.NEXT:
        fp.write(f'{TOPIC},{quota[0]},{quota[1]},{quota[2]},{exp},{info["extra"]}\n')
        print(getHash(exp), file=hash_file)
        hash_data.append(getHash(exp))

fp.close()
hash_file.close()
