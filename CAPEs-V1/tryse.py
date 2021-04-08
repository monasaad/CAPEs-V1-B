import sqlite3
from difflib import SequenceMatcher
import spacy
from flask import session
from textblob import TextBlob
import re

connection = sqlite3.connect('CAPEsDatabase.db')
c = connection.cursor()
nlp = spacy.load("en_core_web_lg")

user_input = "CS"
list_matching = []
listofuserkeyword = []
user_inputAfterSplit = []
user_inputwithoutCorrect = []
c.execute("SELECT keyword FROM keyword Where id_r = ?", [1])
keyword = c.fetchall()  # save result
listUserWord = []
print('input', user_input)
print('keyword from getKeyword()', keyword)
for row in keyword:
    match = SequenceMatcher(None, user_input, row[0]).find_longest_match(0, len(user_input), 0, len(row[0]))
    list_matching.append(row[0][match.b: match.b + match.size])
    list_matching= list(set(list_matching).intersection(set(keyword)))
    #listUserWord= list(set(listofuserkeyword).intersection(set(keyword)))  # new
# add in new list
for word in list_matching:
    for uttrence in user_input.split():
        if uttrence.__contains__(word):
            listUserWord.append(uttrence)

print('befor list_matching from getKeyword()', list_matching)
print(' befor listUserWord from getKeyword()', listUserWord)

# reomve the keyword that found
if list_matching.__len__() != 0:
    for keyw in session['list_matching']:
        user_inputwithoutCorrect = re.split(keyw, user_input)
else:
    user_inputwithoutCorrect = re.split(' ', user_input)

print('without',user_inputwithoutCorrect)
# to correct typo
for word in user_inputwithoutCorrect:
    user_inputAfterSplit.append(str(TextBlob(word).correct()))

print('user_inputAfter',user_inputAfterSplit)
query = 1
wordcount = 0
if not query == 2:
    for patternK in user_inputAfterSplit:
        print(patternK)
        onePattern1 = nlp(patternK.replace(" ", ""))
        for key in keyword:
            if key[0] not in list_matching:
                onePattern = nlp(key[0])
                try:
                    similarity = onePattern1.similarity(onePattern)
                    print('similarity', similarity)
                except UserWarning:
                    similarity = 0
                # keep track of highest score
                if similarity > 0.7:
                    list_matching.append(key[0])
                    listUserWord.append(user_inputwithoutCorrect[wordcount])  # new
        wordcount += 1

print('list_matching from getKeyword()', list_matching)
print('listUserWord from getKeyword()', listUserWord)



