import sqlite3
import sys
conn = sqlite3.connect('./words.db')

c = conn.cursor()

from urllib import parse
def getDescription(id):    
    from SPARQLWrapper import SPARQLWrapper, JSON
    id = parse.quote_plus(id)

    #id = id.replace("\"", "&quot;")
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    query = """
   PREFIX dbres: <http://dbpedia.org/resource/>
   select ?property ?value where {
   <http://dbpedia.org/resource/"""+id+"""> <http://www.w3.org/2000/01/rdf-schema#label> ?value .
   FILTER(LANG(?value) = "" || LANGMATCHES(LANG(?value), "en"))
}
"""
    print(query)
    sparql.setQuery(query)

    sparql.setReturnFormat(JSON)
    print("Retrieving...")
    results = sparql.query().convert()
    
    for result in results["results"]["bindings"]:
        for column in result:
            return result["value"]["value"]
                                                                                       
    return None

c.execute("ALTER dbwords ADD Colu", t)

words = [row[0] for row in c.execute('''SELECT word from dbwords WHERE title is null''')]
for word in words:
    c = conn.cursor()
    try:
        print(word) 
        t = (getDescription(word), word)
        print(t)
        c.execute("UPDATE dbwords SET title=? where word=?", t)
    except:
        print("there was an error",  sys.exc_info())
  
    conn.commit()
    
conn.close()
