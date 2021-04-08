import re

us = 'i love c+++ and ai'

"""a = []
for u in us.split():
    if us.__contains__('c++'):
            a.append(re.split('c\+\+', u)[0])
    else:
            a.append('m')
print(a)"""

list_matching = ['c+++','ai','java']
user_inputwithoutCorrect= []

#user_inputwithoutCorrect.append(re.split('c\+\+', str(us))) # remove the keyword from user input -> pattern

removed_keyword = ' '.join(word for word in us.split() if word not in list_matching)
user_inputwithoutCorrect = removed_keyword.split()

print(user_inputwithoutCorrect)