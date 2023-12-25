
diction = {
        ",":"，",
        " ":"",
        "o":"",
        "e":"",
        "「":"",
        "」":""
}
def parse(token):
    if token == "\n":
        return

    for rep in diction:
        token = token.replace(*rep)

    return token

def load_parse():

    with open("./target", mode='r', encoding='utf-8') as fp:
        buffer = []
        for line in fp:
            out = parse(line)
            if out is None:
                continue
            buffer.append(out)

    with open("./output", mode='w', encoding='utf-8') as fp:
        for line in buffer:
            fp.write(line)


if __name__ == '__main__':
    load_parse()

