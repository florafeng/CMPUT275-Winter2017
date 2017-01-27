# add your solution here
import sys
state = True
count = {}
array = []
output = []

for line in sys.stdin:
    # line = input()
    if (len(line) > 0):
        # print(len(line))
        first = line[0]
        array.append(line.strip())
        if first in count:
            count[first] += 1
        if (first not in count):
            count[first] = 1

min_freq = min(count.values())

for s in array:
    if count[s[0]] == min_freq:
        output.append(s)

# print(output)
print(min_freq)
output = list(set(output))
# print(output)
for each in sorted(output): print(each)
