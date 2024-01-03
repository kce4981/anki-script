import shutil
from enum import Enum
def load_explanatory(file) -> dict:

    SEPERATOR = "："
    exp = [] 

    fp = open(file, mode='r', encoding='utf-8')

    for line in fp:
        try:
            idx = line.index(SEPERATOR)
        except ValueError:
            print(f'ERROR at line : {line}')
        pack = (line[:idx], line[idx+1:].replace("\n", ""))
        exp.append(pack)
    fp.close()
    return exp
        
def load_fulltext(file) -> str:

    buffer = []
    with open(file, mode='r', encoding='utf-8') as fp:
        for line in fp:
            ln = line.replace("\n", "")
            ln = ln.replace("「","")
            ln = ln.replace("」","")
            buffer.append(ln)

    return ''.join(buffer)

def get_text(fulltext, word: str, rang: tuple[int], ocur: int):
    try:
        idx = fulltext.index(word, ocur)
    except ValueError:
        res = ("NOT FOUND","","")
        return res
    ln = len(word)

    left = max(0, idx-rang[0])
    right= min(len(fulltext), idx+rang[1])
    res = (fulltext[left:idx], fulltext[idx:idx+ln], fulltext[idx+ln:right])
    return res


def get_ocur(fulltext, word):
    ocurs = [len(word)*-1]

    while True:
        try:
            ocurs.append(fulltext.index(word, ocurs[-1]+len(word)))
        except ValueError:
            break

    ocurs.pop(0)
    return ocurs

def create_card_view(topic, text: tuple, explain):
    import shutil
    width = shutil.get_terminal_size()[0]
    l,m,r = text

    payload = []
    payload.append(topic)
    payload.append(f'{l}「{m}」{r}'.center(width))
    payload.append(explain.center(width))
    payload.append('-'*width)

    printScreen(payload)

def process_input(**info):
    resp = input()
    status = Status.ADJUST

    notation = 1

    if resp.startswith('l'):
        if resp.startswith('l-'):
            notation = -1 
        info['rng'][1] += int(resp[2:])*notation

    if resp.startswith('r'):
        if resp.startswith('r-'):
            notation = -1 
        info['rng'][0] += int(resp[2:])*notation

    if resp.startswith('extra'):
        info['extra'] = resp[5:]

    if resp.startswith('next'):
        info['idx'] += 1

    if resp == '':
        status = Status.NEXT

    if resp.startswith('jump'):
        status = Status.SKIP

    if resp.startswith('exit'):
        status = Status.EXIT

    if resp.startswith('f'):
        status = Status.ADJUST
        findNextComma(1, **info)

    if resp.startswith('p'):
        status = Status.ADJUST
        findNextComma(-1, **info)

    return status, info

def printScreen(lines: list[str]) -> None:
    import shutil
    height = shutil.get_terminal_size()[1]
    whitespc = (height - len(lines))//2 

    for _ in range(whitespc):
        print()

    for ln in lines:
        print(ln)

    for _ in range(whitespc, whitespc*2):
        print()

def getHash(string):
    import hashlib
    return hashlib.sha256(string.encode('utf-8')).hexdigest()

def findNextComma(direction, **info):
    candidates = ["，", "；", "。", "、", "？", "！"]
    fulltext = info['fulltext']
    if direction > 0:
        idx = info['position'] + info['rng'][1]
    if direction < 0:
        idx = info['position'] - info['rng'][0]
    ln = len(fulltext)
    while True:
        idx += direction
        if idx >= ln:
            info['rng'][1] = ln-1 
            return info

        if idx < 0:
            info['rng'][0] = 0
            return info

        if fulltext[idx] in candidates:
            if direction > 0:
                info['rng'][1] = idx - info['position'] + 1

            if direction < 0:
                info['rng'][0] = info['position'] - idx  

            return info


class Status(Enum):
    START = 0
    NEXT = 1
    ADJUST = 2
    EXIT = 3
    SKIP = 4
