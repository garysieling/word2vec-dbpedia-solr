import sqlite3
import sys
conn = sqlite3.connect('../words.db')

c = conn.cursor()

from urllib import parse
def getDescription(id):    
    from SPARQLWrapper import SPARQLWrapper, JSON
    id = id.replace("\"", "%22") #parse.quote_plus(id)
    #print(id)

    #id = id.replace("\"", "&quot;")
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    query = """
   PREFIX dbres: <http://dbpedia.org/resource/>
   select ?value where {
   <http://dbpedia.org/resource/"""+id+"""> <http://www.w3.org/2000/01/rdf-schema#label> ?value .
   FILTER(LANG(?value) = "" || LANGMATCHES(LANG(?value), "en"))
}
"""
    
    try:
        print(query)
    except:
        print("error printing")

    sparql.setQuery(query)

    sparql.setReturnFormat(JSON)
    print("Retrieving...")
    results = sparql.query().convert()
    
    for result in results["results"]["bindings"]:
        for column in result:
            return result["value"]["value"]
                                                                                       
    return None


words = [row[0] for row in c.execute('''SELECT word from dbwords WHERE title is null''')]
for word in words:
    c = conn.cursor()

    try:
        print(word) 
    except:
        print("error printing word")

    t = (getDescription(word), word)

    try:
        print(t)
    except:
        print("error printing word")

    c.execute("UPDATE dbwords SET title=? where word=?", t)
  
    conn.commit()
    
conn.close()
