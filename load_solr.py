import sqlite3
import sys
import pysolr

solr = pysolr.Solr('http://104.237.151.183:8983/solr/suggestions/', timeout=10)
solr.delete(q='*:*')

conn = sqlite3.connect('../words.db')
c = conn.cursor()

def update(data):
    def getDocument(prefix, row, index):
        (title, word, suggestions, id) = row
        doc = {}
        doc['word'] = ""
        if (title is None):
            title = ""
        if (word is None):
            word = ""

        if (title == ""):
            if (word == ""):
                return ""

            doc['word'] = word
        else:
            doc['word'] = title

        doc['suggestions'] = suggestions

        if (suggestions == ""):
            return ""

        if (suggestions is None):
            return ""

        shouldCommit = ((index % 1000) == 0)

        doc['id'] = prefix + str(id)

        solr.add([doc], commit=shouldCommit)

    for i, row in enumerate(data):
        try:
            getDocument('a', row, i)
        except:
            print("an error")

    solr.commit()

update([row for row in c.execute('''SELECT title, word, suggestions, id from dbwords''')])

#[getDocument('b', row) for row in c.execute('''SELECT word as title, word as word, suggestions, id from words''')]
#solr.commit()



conn.close()
