# Add your code here
import sys
array = []

s = input()
s.strip()
s = ''.join([i for i in s if not i.isdigit()])
substring = s
z = 0
counter = 0

while True:
    if len(substring) == 0:
        break

    #compare
    while z <= len(substring)-1:
        if substring[z] == s[z]:
            counter += 1
        else:
            break
        z += 1

    array.append(str(counter))
    z = 0
    counter = 0

    #remove
    substring = substring[1:]

output = ' '.join(i for i in array)
print(output)
