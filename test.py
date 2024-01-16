from string import ascii_letters, printable
diction = {key: "" for key in printable}
diction["﹁"] = "「"
diction["﹂"] = "」"
diction["︵"] = "("
diction["︶"] = ")"
diction["\n"] = ""
diction["。"] = "。\n"
newfp = open("./out", mode='w', encoding='utf-8')
with open("./explain.md", mode='r+', encoding='utf-8') as fp:
    buffer = []
    for line in fp.read().splitlines():
        if set(line).issubset(set(ascii_letters) | {" "}):
            continue

        for d in diction.items():
            line = line.replace(*d)

        buffer.append(line)

    # buffer = buffer[::-1]

    for ln in buffer:
        print(ln, end="", file=newfp)
newfp.close()