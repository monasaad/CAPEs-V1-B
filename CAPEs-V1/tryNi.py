import time
import nltk
import sqlite3
from nltk.stem.lancaster import LancasterStemmer
import re
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
import spacy

training_dataP = []
rule = []
final_results = {}
ans_words = {}
high_similarity = 0
patternKey = ' '
counter = 0
similar = 0.0
clearP = 0.0
upload = 0.0
countS = 0.0
countp = 0.0
countL = 0.0
ruleT = 0
contg1 = 0
contg2 = 0
getg = 0
contextg = 0

# open database connection, and make a cursor
connection = sqlite3.connect('CAPEsDatabase.db')
c = connection.cursor()
nlp = spacy.load("en_core_web_lg")


# to take the pttern from database
def getdataPattern(id_r):
    # start_time = time.time()
    global training_dataP
    training_dataP = []
    value = (id_r,)
    c.execute("SELECT id_r, pattern FROM pattern1 Where id_r = ?", value)
    pattern = c.fetchall()
    for row in pattern:
        training_dataP.append({"rule": row[0], "ans": row[1]})
    # end_time = time.time()
    # print("getdatapattern() exution time: ", end_time-start_time)


def getdataGenral(id_c):
    global getg
    global contg2
    # start_time = time.time()
    global training_dataP
    training_dataP = []
    value = (id_c,)
    c.execute("SELECT id_r, pattern FROM pattern1 Where id_c=? ", value)
    pattern = c.fetchall()
    for row in pattern:
        training_dataP.append({"rule": row[0], "ans": row[1]})
    # end_time = time.time()
    # getg += (end_time-start_time)
    contg2 += 1
    # print("getdatagenral() exution time: ", end_time - start_time)


def rules():
    global ruleT
    # start_time = time.time()
    global rule
    c.execute("SELECT question FROM rule")
    for row in c.fetchall():
        rule += [row]
    # end_time = time.time()
    # ruleT += (end_time-start_time)
    # print("rule() exution time: ", end_time-start_time)


# exit the chat
def exitProgram(x):
    # start_time = time.time()
    if x == 'q':
        print("CAPEs: conversation ends. Your records are saved in logs.")

    # end_time = time.time()
    # print("exitprogram() exution time: ", end_time - start_time)


# make each word back to root -using with lema-
def get_wordnet_pos(word):
    # start_time = time.time()
    """Map POS tag to first character lemmatize() accepts"""
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}
    # end_time = time.time()
    # print("get_wordnet_pos() exution time: ", end_time - start_time)
    return tag_dict.get(tag, wordnet.NOUN)


# remove ?/...
def remove_special_characters(user_input):
    # start_time = time.time()
    pattern = r'[^a-zA-z0-9#+\s]'
    user_input_removed_char = re.sub(pattern, ' ', user_input)
    # end_time = time.time()
    # print("remove_special_characters() exution time: ", end_time - start_time)
    return user_input_removed_char


# use word.net to make each word back to root
def lemmatize_text(text):
    # start_time = time.time()
    lemmatizer = WordNetLemmatizer()
    text = ' '.join(lemmatizer.lemmatize(w, get_wordnet_pos(w)) for w in nltk.word_tokenize(text))
    # end_time = time.time()
    # print("lemmatize_text() exution time: ", end_time - start_time)
    return text


def cleardatapatterns():
    global countp
    global clearP
    # start_time = time.time()
    global ans_words
    ans_words = {}
    # turn a list into a set (of unique items) and then a list again (this removes duplicates)
    ans = list(set([a['ans'] for a in training_dataP]))
    # loop through each sentence in our training data
    for c in ans:
        # prepare a list of words within each class like ans_word[my major is]=[]
        ans_words[c] = []
    for pattern in ans:
        # tokenize each sentence into words
        word1 = lemmatize_text(str(pattern))
        # ignore a some things like >?!
        patternAfterClear = remove_special_characters(word1.lower())
        # add the word pattern to our words in class list
        ans_words[pattern].extend([patternAfterClear])
    # end_time = time.time()
    # clearP += (end_time - start_time)
    countp += 1
    # print("cleardatapatterns() exution time: ", end_time - start_time)


# calculate a score for a given class taking into account word commonality
def similarity_method(userSentence):
    global countS
    global similar
    # start_time = time.time()
    global high_similarity
    global patternKey
    high_similarity = 0
    patternKey = ' '
    usertokan = nlp(userSentence)
    # tokenize each word in our user sentence
    for patternK in ans_words:
        for pattern in ans_words[patternK]:
            onePattern = nlp(pattern)
            try:
                similarity = usertokan.similarity(onePattern)
            except UserWarning:
                similarity = 0

            # keep track of highest score
            if similarity > high_similarity:
                patternKey = patternK
                high_similarity = similarity
    # end_time = time.time()
    countS += 1
    # similar += (end_time-start_time)
    # print("similarity_method() exution time: ", end_time - start_time)


def genralContaxt(count, user_input, questions):
    global contextg
    global contg1
    # start_time = time.time()
    getdataGenral(2)
    cleardatapatterns()
    similarity_method(user_input)
    if high_similarity > 0.9:
        print("genral")
        uploadLog(questions, user_input, patternKey, high_similarity, 'general')
        # end_time = time.time()
        # contextg += (end_time - start_time)
        contg1 += 1
        # print("genralContaxt() exution time: ", end_time - start_time)
        responesive(count)
    else:
        print("CAPEs: Sorry I did not get that :(")
        uploadLog(questions, user_input, patternKey, high_similarity, 'Sorry I did not get that :(')  # 0
        # end_time = time.time()
        # contextg += (end_time-start_time)
        contg1 += 1
        # print("genralContaxt() exution time: ", end_time - start_time)
        responesive(count)


def responesive(coun):
    getdataPattern(coun + 1)
    cleardatapatterns()
    if coun == 6:
        # result
        print("thank you")

    else:
        questions = ''.join(rule[coun])
        user_in = input("CAPEs: " + questions).lower()
        user_str = str(user_in)
        # user_inputs = ['cs', 'level 1', 'database','c', 'no', 'long']
        # users_input = ''.join(user_inputs[coun]).lower()
        user_input = remove_special_characters(lemmatize_text(user_str))
        exitProgram(user_input)
        similarity_method(user_input)

        if high_similarity > 0.9:
            # final_results.append(coun+1,patternKey)
            final_results[coun + 1] = [patternKey]
            # print(final_results)
            uploadLog(questions, user_input, patternKey, high_similarity, 'go to next question')
            responesive((coun + 1))
        else:
            # genarla
            genralContaxt(coun, user_input, questions)


def uploadLog(ques, ansQ, matched, similartiy, response):
    global upload
    global countL
    # start_time = time.time()
    data_t = (ques, ansQ, matched, similartiy, response)
    c.execute("INSERT INTO log (question, userAns, matched_text, similarity , response) VALUES (?,?,?,?,?)", data_t)
    connection.commit()
    # end_time = time.time()
    # upload += (end_time-start_time)
    countL += 1
    # print("uploadLog() exution time: ", end_time - start_time)


# the worker
print('CAPES: Hello there I\'m CAPEs! I\'m an artificial advisory I can recommend for you' \
      'professional exams and certificates. ' \
      '\nTo help you in that I need information for you are your ready?' \
      '\nIf you want to exist and save your progress please click q')
rules()
# start_time = time.time()
responesive(counter)
# end_time = time.time()
# print("responesive() exution time: ", end_time - start_time)
# print("uploadLog() exution time: ", upload/countL)
# print("similarity_method() exution time: ", similar/countS)
# print("cleardatapatterns() exution time: ", clearP/countp)
# print("rule() exution time: ", ruleT)
# print("getdatagenral() exution time: ", getg/contg2)
# print("genralContaxt() exution time: ", contextg/contg1)
