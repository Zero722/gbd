list1 = ["apple","banana"]
list1.append("cat")
print(list1[-1])
print(list1)
print (type(list1))
list2 = list1.copy()
list1.append("Dog")
print(list2)
print(len(list2))
print("apple" in list1)
list1.insert(0, "axe")
list1[1] = "berry"
print(list1[:3])
list1.extend(list2)
print(list1)
list1.remove("banana") #only removes the first "banana"
list1.pop()
list1.pop(3)
print(list1)
list2.clear()
print(list2)
del list2
# print(list2) #gives not defined

list1.sort()
print(list1)

list3 = [100, 50, 49, 51, 65, 82, 23]

list3.reverse()
print(list3)

list3.sort()
print(list3)

list3.sort(reverse = True)
print(list3)

def myfunc(n):
  return abs(n - 50)

list3.sort(key = myfunc)
print(list3)