# put your code here
import sys
array = []

for line in sys.stdin:
     if line.strip():
         counter = 0
         reached = set()

         for c in line.strip().lower():
             if (c in "vkjxqz") and (c not in reached):
                #  print("in")
                 counter += 1
                 reached.update(c)

         if counter > 4:
             array.append("BAD")
            #  print("bad")
         elif counter <= 4:
             array.append("OK")
            #  print("ok")

for ele in array:
    print(ele)
