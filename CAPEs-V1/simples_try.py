import re

array = {1: ['@cs and', '* ai'], 2: ['@2 and @4', '* 3']}
array1 = {}


def nextword(idQ, target, pattern):
    for i, w in enumerate(pattern):

        if w == target:
            if idQ in array.keys():
                array1[idQ].append(pattern[i+1])
            else:
                array1[idQ] = [pattern[i + 1]]


def takeKey(row):
    for pattern in row:
        nextword(row, '*', pattern.split())


def wordofq(x):
    takeKey(array[1])


#wordofq(1)
res= array[2][0].partition('*')[2]
print(res)
result = re.findall(r"^@\w+", array[2][0])
print(result)
