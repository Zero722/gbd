from django.test import TestCase

# Create your tests here.
def test1(x, **data):
    # print(x)
    if "color" in data.keys():
        return x, data["color"]
    else:
        return x

a = test1(1)
print(a)
