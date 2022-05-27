list1 = ["apple", "banana",  "cat", "dog"]

iter1 = iter(list1)
print(next(iter1))
print(next(iter1))
print(next(iter1))

iter2 = iter(list1[0])
print(next(iter2))
print(next(iter2))
print(next(iter2))
print(next(iter2))
print(next(iter2))

for i in list1:
    print(i)

for i in range(4):
    print(list1[i])


# Creating iterator
class MyNumbers:
  def __iter__(self):
    self.a = 1
    return self

  def __next__(self):
    x = self.a
    self.a += 1
    return x

myclass = MyNumbers()
myiter = iter(myclass)

print(next(myiter))
print(next(myiter))
print(next(myiter))
print(next(myiter))
print(next(myiter))

for i in myclass:
    if i == 10:
        break
    print("Number: ",i)


class MyNum:
  def __iter__(self):
    self.a = 1
    return self

  def __next__(self):
    if self.a <= 20:
      x = self.a
      self.a += 1
      return x
    else:
      raise StopIteration

myclass = MyNum()
myiter = iter(myclass)

for x in myiter:
  print("Num: ",x)



d = {"name": "Utsav", "lname": "Nayaju"}
 
for i in d:
    print(i,":",d[i])

for i,j in d.items():
    print(i,":",j)