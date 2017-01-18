# slpit returns a list of tokens, token is a string
tokens = input().split()
chocolates = int(tokens[0])
jars = int(tokens[1])
count = 0

# write your code here
for i in range(0, jars):
    a = input().split()
    cur = int(a[0])
    max = int(a[1])
    if (cur+chocolates) <= max:
        count += 1
    del a
    del cur
    del max

print(count)
    
