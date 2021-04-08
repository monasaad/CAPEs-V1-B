# spacy takes more than 10s to print the result كنسل يامدير
import spacy


nlp = spacy.load("en_core_web_lg")
tokensq = nlp("my major is")
tokens = nlp("it major")
print(tokens.similarity(tokensq))

"""
# Program to measure similarity between
# two sentences using cosine similarity.
import spatial as spatial

import nltk
nltk.download('stopwords')

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# X = input("Enter first string: ").lower()
# Y = input("Enter second string: ").lower()
X = "I love horror movies"
Y = "Lights out is a horror movie"

# tokenization
X_list = word_tokenize(X)
Y_list = word_tokenize(Y)

# sw contains the list of stopwords
sw = stopwords.words('english')
l1 = [];
l2 = []

# remove stop words from string
X_set = {w for w in X_list if not w in sw}
Y_set = {w for w in Y_list if not w in sw}

# form a set containing keywords of both strings
rvector = X_set.union(Y_set)
for w in rvector:
    if w in X_set:
        l1.append(1)  # create a vector
    else:
        l1.append(0)
    if w in Y_set:
        l2.append(1)
    else:
        l2.append(0)
c = 0

# cosine formula
for i in range(len(rvector)):
    c += l1[i] * l2[i]
cosine = c / float((sum(l1) * sum(l2)) ** 0.5)
print("similarity: ", cosine)"""
"""import spacy

nlp = spacy.load('en_core_web_md')

doc1 = nlp(u'Hello this is document similarity calculation')
doc2 = nlp(u'Hello this is python similarity calculation')
doc3 = nlp(u'Hi there')

print(doc1.similarity(doc2))
print(doc2.similarity(doc3))
print(doc1.similarity(doc3))

vector1 = [1, 2, 3]
vector2 = [3, 2, 1]

cosine_similarity = spatial.distance.cosine(vector1, vector2)
print(cosine_similarity)"""