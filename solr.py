import sqlite3
import sys

conn = sqlite3.connect('./words.db')

c = conn.cursor()

num = 0
lookup = {}
words = [row for row in c.execute('''SELECT word, title, id from dbwords''')]
for row in words:
    word = row[0]
    id = 'x' + str(num) + 'x'
    t = (id, word)
    
    num = num + 1
    lookup[id] = word
    c.execute("UPDATE dbwords SET id=? where word=?", t)

conn.commit()

from gensim.models import Word2Vec
model = Word2Vec.load("/root/.ssh/en_1000_no_stem/en.model")

words = [row for row in c.execute('''SELECT word, title, id from dbwords''')]

epsilon = 0.65
for row in words:
    word = row[0]
    title = row[1]

    c = conn.cursor()

    near = model.wv.most_similar(['DBPEDIA_ID/' + word], topn=100)
    query = ""
    for t in near:
        (w, d) = t
        query = query + lookup[w] + "^" + str(d + epsilon)[0:4] + " "

    query = query[:-1]
    print(query)

    t = (id, query, word)
    print(t)
    c.execute("UPDATE dbwords SET query=? where word=?", t)
  
    conn.commit()
    
conn.close()
