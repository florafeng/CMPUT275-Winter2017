# read number of friends
num_friends = int(input())
array = [None] * num_friends

# for each friend, read their numbers..
for i in range(num_friends):
    # input().split() is fine
    num_fav = input().strip().split()
    array[i] = num_fav

# read the index of friend whose numbers should be printed
index = int(input())

# print the favourite numbers of the selected friend
pointer = 1
end = len(array[index])-1
while pointer <= (end):
    if pointer == (end): # if it's the end of output, no space!!
        print(array[index][pointer], end="")
    else:
        print(array[index][pointer], end=" ")
    pointer += 1
print()

# alternate method
print(" ".join(array[index]))
          # do   # interater
list( map( int, array[index]) )
