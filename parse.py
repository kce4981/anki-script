
diction = {
        ",":"，",
        " ":"",
        "o":"",
        "e":"",
        "「":"",
        "」":"",
        "于":"於" # 破爛簡繁轉換，于根本不通繁體
        
}
def parse(token):
    if token == "\n":
        return

    for rep in diction.items():
        token = token.replace(*rep)

    return token

def load_parse():

    with open("./explain.md", mode='r', encoding='utf-8') as fp:
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

