import sys

filename = "classify_proposals.py"
with open(filename, "r") as f:
    lines = f.readlines()

new_lines = []
skip = False
for line in lines:
    if "for f in args.files:" in line:
        new_lines.append(line)
        new_lines.append("""        result = classify_file(f)

        color = Palette.GREEN if "Flex" in result else Palette.CYAN
        formatted_result = Palette.colorize(result, color)

        if "Flex" in result:
            flex_count += 1
        elif "Respond" in result:
            respond_count += 1

        if os.path.exists(f):
            print(f"📄 {f}: {formatted_result}")
        else:
            # Handle the missing files mentioned by user
            # We still count them as they were classified by name
            error_msg = Palette.colorize("(File not found)", Palette.RED)
            print(f"❌ {f} {error_msg}: {formatted_result}")\n""")
        skip = True
    elif "print(f\"\\n{Palette.BOLD}Summary:{Palette.RESET}\")" in line:
        skip = False
        new_lines.append(line)
    elif not skip:
        new_lines.append(line)

with open(filename, "w") as f:
    f.writelines(new_lines)
