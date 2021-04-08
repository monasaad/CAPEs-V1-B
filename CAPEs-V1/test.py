import random
import en_core_web_lg
import nltk
import sqlite3
import re
from nltk import WordNetLemmatizer

# COMPLETED FUNCTIONS :)
# 1. exit the program
# 2. extract the keywords from user input, match it with predefined keyword table
# 3. ignore the keywords from user input
# 4. check the user input similarity with predefined pattern table
# 5. define a query for both getKeyword & similarityCheck with one parameter
# 6. save the inputs to logs
# 7. add user's input into SQL query, if exist return certificate name. if not return sorry
# 8. handle special characters - exception (c++, c#, etc)

# PENDING FUNCTIONS :)
# 1. handle typos - CAPES V2
# 2. handle negation - CAPES V2
# 3. handle general utterances - waiting for D&S

nlp = en_core_web_lg.load()

# open database connection, and make a cursor
connection = sqlite3.connect('CAPEsDatabase.db')
cursor = connection.cursor()

# sql query to get keywords, add the result in a list، change query upon user_input
cursor.execute("SELECT keyword FROM keyword")
keywords_list = [i[0] for i in cursor.fetchall()]

# sql query to get pattern, change query upon user_input
cursor.execute("SELECT anwser_p FROM pattern")
pattern_result = cursor.fetchall()

# sql query to get questions, change query upon user_input
cursor.execute("SELECT question FROM questions")
questions_result = cursor.fetchall()

random = random.randint(0, 10000)


# exit the chat
def exitProgram(x):
    if x == 'q':
        print("CAPES: conversation ends. Your records are saved in logs.")
        exit()


# 1. find keyword
# 1.2 get the keywords from database and compare them with user input
# V2: handle typos
def getKeyword(user_input):
    # lemmatize the user input first, I cannot call it bc it's calls other methods
    user_input_tokenized = user_input.split()
    user_input_list = list(user_input_tokenized)
    # find the intersection between user input list and keywords list
    list_matching = list(set(user_input_list).intersection(set(keywords_list)))
    return list_matching


# 2. find pattern similarity (3 steps for cleaning)
# 2.1 remove keywords from user input
def removeKey(user_input):
    keywords = getKeyword(user_input)
    removed_keyword = ' '.join(word for word in user_input.split() if word not in keywords)
    return removed_keyword


# 2.2 remove special characters from user input
def removeSpecialCharacters(user_input):
    pattern = r'[^a-zA-z0-9\s]'  # what does it mean??
    user_input_removed_char = re.sub(pattern, '', user_input)
    return user_input_removed_char


# 2.3 lemmatize user input, make each word back to root
def lemmatize(user_input):
    lemmatizer = WordNetLemmatizer()
    user_input_lemmatized = ' '.join(lemmatizer.lemmatize(w) for w in nltk.word_tokenize(user_input))
    return user_input_lemmatized


# 2.4 get the patterns from database and compare them with user input, get the most matching pattern similarity -
# only to save it in logs-
# we should lemmatize pattern in the database, done
def patternSimilarity(user_input):
    user_input = lemmatize(removeSpecialCharacters(removeKey(user_input)))  # cleaning
    token1 = nlp(user_input)  # load to the model
    similarity_list = []
    for row in pattern_result:
        token2 = nlp(lemmatize(row[0]))
        similarity = token1.similarity(token2)
        similarity_list.append(similarity)
    return max(similarity_list)


def question():
    for row in questions_result:
        questions = ''.join(row[0])
        user_input = input(questions).lower()
        exitProgram(user_input)

        if patternSimilarity(user_input) < 0.7:
            print("CAPES: Sorry I did not get that :(")
            # decrement the loop, to go to the previous question

        # solve this, add more
        if user_input == "no":
            keywords = None

        # only used to upload log
        pattern_similarity = patternSimilarity(user_input)
        keywords = " ".join(getKeyword(user_input))
        user_input_removed_keywords = "".join(removeKey(user_input))
        data = (random, user_input, user_input_removed_keywords, keywords, pattern_similarity, questions)

        cursor.execute("INSERT INTO log (qNumer, userAns, textWithOutKey, keywords , patternAsimilarity, question) "
                       "VALUES (?, ?, ?, ?, ?, ?)", data)
        connection.commit()
    return random


# 3. find certificate
def findCertificate():
    cursor.execute("SELECT keywords FROM log WHERE qNumer=?", [random])

    result = cursor.fetchall()
    key_list = []

    for row in result:
        key_list.append(row[0])

    """cursor.execute("SELECT certificate_name  FROM certificate WHERE (major =? AND level =? AND field =? AND "
                   "pre_certificate =? AND porgram_L =? AND vendor =? AND duration=?)",
                   (key_list[0], key_list[1], key_list[2], key_list[3], key_list[4], key_list[5], key_list[6]))"""

    cursor.execute("SELECT certificate_name  FROM certificate WHERE (level =?)", (key_list[0]))
    results = cursor.fetchall()

    print("CAPEs: I found the most matching certificate for you: ")
    for row in results:
        print("-", row[0])


"""# 4. save results in logs
def uploadLog(user_input):
    keywords = " ".join(getKeyword(user_input))
    user_input_removed_keywords = "".join(removeKey(user_input))
    pattern_similarity = patternSimilarity(user_input)
    questions_list = question()

    data = (user_input, user_input_removed_keywords, keywords, pattern_similarity, questions_list)
    cursor.execute(
        "INSERT INTO log (userAns, textWithOutKey, keywords , patternAsimilarity, question) VALUES (?, ?, ?, ?, ?)",
        data)
    print("success")"""

major = "my majors is AI and CS +-".lower()

question()
findCertificate()