import sqlite3
import sys
import json

conn = sqlite3.connect('./words.db')

c = conn.cursor()

from gensim.models import Word2Vec
model = Word2Vec.load("/root/.ssh/en_1000_no_stem/en.model")

words = [row for row in c.execute('''SELECT word, id from words''')]

for row in words:
    word = row[0]

    c = conn.cursor()

    near = model.wv.most_similar([word], topn=10)
    query = ""
    suggestions = []
    for t in near:
        (w, d) = t
        title = ""
        if (w[0:11] == "DBPEDIA_ID/"):
            t2 = (w[11:],)
            first = [row for row in c.execute('''SELECT title from dbwords where word=?''', t2)][0]
            (t,) = first
            title = t

            if (title == None):
                title = w[11:].replace("_", " ")
        else:
            title = w
            
        suggestions.append(title)

    suggestions = json.dumps(suggestions)
    print("suggestions (1): " + suggestions)
    t3 = (suggestions, word)    

    c.execute("UPDATE words SET suggestions=? where word=?", t3)
  
    conn.commit()
 

words = [row for row in c.execute('''SELECT word, title, id from dbwords''')]

for row in words:
    word = row[0]

    c = conn.cursor()

    near = model.wv.most_similar(['DBPEDIA_ID/' + word], topn=10)
    query = ""
    suggestions = []
    for t in near:
        (w, d) = t
        title = ""
        if (w[0:11] == "DBPEDIA_ID/"):
            t2 = (w[11:],)
            first = [row for row in c.execute('''SELECT title from dbwords where word=?''', t2)][0]
            (t,) = first
            title = t

            if (title == None):
                title = w[11:].replace("_", " ")
        else:
            title = w
            
        suggestions.append(title)

    suggestions = json.dumps(suggestions)
    print("suggestions (2): " + suggestions)
    t3 = (suggestions, word)    

    c.execute("UPDATE dbwords SET suggestions=? where word=?", t3)
  
    conn.commit()
    
conn.close()
