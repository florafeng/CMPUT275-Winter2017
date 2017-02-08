# Put your code here
first_line = input().split( )
array = []
match_array = []
return_array = []
for line in range(int(first_line[0])):
    line = input()
    array.append(line)

for match in range(int(first_line[1])):
    match = input()
    match_array.append(match)

def compare(match, original):
    counter = 0
    for pos in range(len(match)):
        if match[pos] == '?':
            counter += 1
        elif match[pos] == original[pos]:
            counter += 1

    if counter == len(match):
        curr_array.append(original)

for ele in match_array:
    curr_array = []
    for ele1 in array:
        if len(ele) == len(ele1):
            compare(ele, ele1)
    return_array.append(curr_array)

for arr in return_array:
    arr = sorted(arr)
    print(' '.join(arr))
