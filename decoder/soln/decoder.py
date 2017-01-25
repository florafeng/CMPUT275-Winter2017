# read code->word map
n = int(input())
code2word = dict()
input_dict = {}

# read encoded sentence
for i in range(n):
    line = input().split()
    input_dict[line[0]] = line[1]

# decode sentence
code = input()
pointer = 0
output_list = []

for j in range(len(code)+1):
    key = code[pointer:j]
    if key in input_dict:
        output_list.append(input_dict[key])
        pointer = j

print(' '.join(output_list))
