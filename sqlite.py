import sqlite3
conn = sqlite3.connect('./words.db')

import gensim

#model = gensim.models.KeyedVectors.load_word2vec_format('freebase-vectors-skipgram1000-en.bin',binary=True)
#list(model.vocab.keys())[:100]

from gensim.models import Word2Vec
model = Word2Vec.load("/root/.ssh/en_1000_no_stem/en.model")

c = conn.cursor()

c.execute('''DROP TABLE IF EXISTS dbwords;''')
c.execute('''DROP TABLE IF EXISTS words;''')
c.execute('''CREATE TABLE IF NOT EXISTS dbwords (word text, title text)''')
c.execute('''CREATE TABLE IF NOT EXISTS words (word text)''')

for key in model.wv.vocab:
  if (key.startswith("DBPEDIA_ID/")):
    t = (key[11:],)
    c.execute("INSERT INTO dbwords (word) VALUES (?)", t)
  else:
    t = (key,)
    c.execute("INSERT INTO words (word) VALUES (?)", t)

  conn.commit()
                                            
conn.close()
