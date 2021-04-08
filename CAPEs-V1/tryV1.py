import nltk
import sqlite3
from nltk.stem.lancaster import LancasterStemmer
import re
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet

training_dataP = []
training_dataK = []
listK = []
# save every utterance on it for all the patterns
corpus_words = {}
# save every utterance on it for specific the pattern like ans_word['my major is']=['my','major','is']
ans_words = {}


# open database connection, and make a cursor
connection = sqlite3.connect('CAPEsDatabase.db')
c = connection.cursor()


# to take the pttern from database
def getdataPattern(id_r):
    global training_dataP
    value = (id_r,)
    c.execute("SELECT id_r, anwser_p FROM pattern Where id_r = ?", value)
    pattern = c.fetchall()
    for row in pattern:
        training_dataP.append({"rule": row[0], "ans": row[1]})


# to take the keywords from database
def getdataKeyWord(id_r):
    global training_dataK
    value = (id_r,)
    c.execute("SELECT id_r, keyword FROM keyword Where id_r = ?", value)
    keywords = c.fetchall()
    for row in keywords:
        training_dataK.append({"rule": row[0], "key": row[1]})


# make each word back to root -using with lema-
def get_wordnet_pos(word):
    """Map POS tag to first character lemmatize() accepts"""
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}

    return tag_dict.get(tag, wordnet.NOUN)


# remove ?/...
def remove_special_characters(text):
    pattern = r'[^a-zA-z0-9\s]'
    text = re.sub(pattern, '', text)
    return text


# use word.net to make each word back to root
def lemmatize_text(text):
    lemmatizer = WordNetLemmatizer()
    text = ' '.join(lemmatizer.lemmatize(w, get_wordnet_pos(w)) for w in nltk.word_tokenize(text))
    return text


# her the corpus_words and ans_word will fill with clear pattern
def cleardatapatterns():
    global corpus_words
    global ans_words
    # turn a list into a set (of unique items) and then a list again (this removes duplicates)
    ans = list(set([a['ans'] for a in training_dataP]))
    for c in ans:
        # prepare a list of words within each class like ans_word[my major is]=[]
        ans_words[c] = []
    # loop through each sentence in our training data
    for pattern in training_dataP:
        # tokenize each sentence into words
        for wordinPattern in nltk.word_tokenize(pattern['ans']):
            word1 = lemmatize_text(wordinPattern)
            # ignore a some things like >?!
            word2 = remove_special_characters(word1.lower())
            # have we not seen this word already? add to corpus_words else increment the count
            if word2 not in corpus_words:
                corpus_words[word2] = 1
            else:
                corpus_words[word2] += 1
            # add the word pattern to our words in class list
            ans_words[pattern['ans']].extend([word2])


# calculate a score for a given class taking into account word commonality
def calculate_class_score(userSentence, pattern, show_details=True):
    score = 0
    countOfwords = 0
    # tokenize each word in our user sentence
    for word in nltk.word_tokenize(userSentence):
        countOfwords += 1
        if word.lower() in ans_words[pattern]:
            # treat each word with relative weight
            # score += (1 / corpus_words[stemmer.stem(word.lower())])
            score += 1
            if show_details:
                print("   match: %s (%s)" % (word.lower(), score))
    # simmalrity = score / countOfwords
    return score / countOfwords


# take the max similarity
def classify(userSentence):
    high_class = None
    high_score = 0
    # loop through our paternKey
    for patternKey in ans_words.keys():
        # calculate score of sentence for each class
        score = calculate_class_score(userSentence, patternKey, show_details=False)
        # keep track of highest score
        if score > high_score:
            high_class = patternKey
            high_score = score
    return high_class, high_score


def getKeyword(text):
    global listK
    keyword = list(set([a['key'] for a in training_dataK]))
    for word in text.split():
        for key in keyword:
            if word == key:
                listK = [word]
    return listK


def removeKey(text):
    listk = getKeyword(text)
    resultwords = [word for word in text.split() if word not in listk]
    text = ' '.join(resultwords)
    return text


def uploadLog(ansQ, id_r):
    # upload to database
    textOkey = removeKey(ansQ)
    match = str(classify(remove_special_characters(lemmatize_text(textOkey))))
    keywodINuser = ', '.join(e for e in listK)
    data_t = (id_r, ansQ, textOkey, keywodINuser, match)
    c.execute("INSERT INTO log (qNumer, userAns, textWithOutKey, keywords , patternAsimilarity) VALUES (?,?,?,?,?)",
              data_t)



def short(id_r, ansq):
    getdataPattern(id_r)
    getdataKeyWord(id_r)
    cleardatapatterns()
    uploadLog(ansq, id_r)


major = input('CAPES: 1. What is your major?\n').lower()
short(1, major)
print(training_dataK)
print(removeKey(major))
print(getKeyword(major))
print(listK)

"""level = input("CAPES: 2. In which level are you?\n").lower()
short(2, level)

field = input("CAPES: 3. Which fields are you interested in?\n").lower()
short(3, field)

pre_certificate = input("CAPES: 4. Do you have any pre-certificate, if yes please specify?\n").lower()
short(4, pre_certificate)

porgram_L = input("CAPES: 5. What are programming languages you prefer to use?\n").lower()
short(5, porgram_L)

vendor = input("CAPES: 6. Do you have a specific vendor?\n").lower()
short(6, vendor)

duration = input("CAPES: 7. Do you prefer long-term or short-term study?\n").lower()
short(7, duration)"""
