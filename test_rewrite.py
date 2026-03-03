filename = "classify_proposals.py"
with open(filename, "r") as f:
    lines = f.readlines()
for i, line in enumerate(lines[164:193]):
    print(f"{i+165}: {line}", end='')
