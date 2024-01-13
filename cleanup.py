import pathlib

root = pathlib.Path(__file__).parents[0]
files = [ root / "explain.md", root / "out.csv", root / "fulltext"]
#files = [ root/ "test" ]

target = input("What name do you want you folder to be called (in a/b formats): ").split("/")

new_dir = root / "archive" / '/'.join(target)
new_dir.mkdir(parents=True)
for file in files:
    file.rename(root / new_dir / file.name)

if input("Do you want to create new files: ").lower() != 'yes':
    exit()

for file in files:
    file.touch()
