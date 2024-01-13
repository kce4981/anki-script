from string import ascii_letters
with open("./explain.md", mode='r+', encoding='utf-8') as fp:
    buffer = []
    for line in fp.read().splitlines():
        if set(line).issubset(set(ascii_letters) | {" "}):
            continue

        buffer.append(line)

    buffer = buffer[::-1]

    for ln in buffer:
        print(ln, file=fp)
