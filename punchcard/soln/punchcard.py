import sys

inside = False
for line in sys.stdin:
    line = line.strip()

    if len(line) != 0:
        # get bit length
        if line[0].isdigit():
            bit_length = int(line[0]) + 1

        # check if line is empty
        if line == "":
            continue

        if line[0] == '-' and inside:
            inside = False
            print()

        # get output char and print
        if line[0] == '|':
            curr_line = line[0:-1:2]
            curr_line = curr_line.replace("|", "")
            curr_line = curr_line.replace("o", "1")
            curr_line = curr_line.replace(" ", "0")
            output_char = chr(int(curr_line, base=2))
            inside = True
            print(output_char, end='')
