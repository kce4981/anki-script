import shutil
def load_explanatory(file) -> dict:

    SEPERATOR = "："
    exp = {} 

    fp = open(file, mode='r', encoding='utf-8')

    for line in fp:
        try:
            idx = line.index(SEPERATOR)
        except ValueError:
            print(f'ERROR at line : {line}')
        exp[line[:idx]] = line[idx+1:].replace("\n", "")
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
    width, height = shutil.get_terminal_size()
    l,m,r = text


    print(topic)
    print(f'{l}「{m}」{r}'.center(width))
    print(explain.center(width))
    print('-'*width)

def process_user_input(nont, rng, extra, jump_flag):
    resp = input()
    status = False
    if resp == '':
        status = True

    if resp.startswith('l'):
        if resp.startswith('l-'):
            nont = -1 
        rng[1] += int(resp[2:])*nont

    if resp.startswith('r'):
        if resp.startswith('r-'):
            nont = -1 
        rng[0] += int(resp[2:])*nont

    if resp.startswith('extra'):
        extra = resp[5:]

    if resp.startswith('jump'):
        jump_flag = True
        status = True

    if resp.startswith('exit'):
        status = None


    pack = nont, rng, extra, jump_flag, status
    return pack
