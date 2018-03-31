from neo4jrestclient.client import GraphDatabase
import json
from py2neo import Graph, Node, Relationship, authenticate
import random
authenticate("52.35.21.1:7474","neo4j", "scibase")
graph=Graph("http://52.35.21.1:7474/db/data")
cypher = graph.cypher

numberOfAuthors = 100

def i10(x):
    citationList = []
    node = 'A'+str(x)
    print("calculating for %s"%node)
    findArticles = 'MATCH (u:Author)-[:AUTHORED_BY]->(m:Article) WHERE u.Name = "%s" RETURN m.Name'%node
    value = cypher.execute(findArticles)
    for x in value:
        a=x[0].encode("utf-8")
        findCitedArticles = 'MATCH (n:Article {Name:"%s"})<-[r:CITED_BY]-(m:Article) RETURN COUNT(r)'%(a)
        articles = cypher.execute(findCitedArticles)
        citationList.append(articles[0][0])
    citationList.sort(reverse=True)
    i10 = indexCalculation(citationList)
    print(i10)
    authorUpdate = 'MATCH (n:Author) where n.Name="%s"SET n.i10=%d;'%(node, i10)
    cypher.execute(authorUpdate)

def indexCalculation(x):
    i10 = 0
    print(x)
    for j in x:
        if(j>10):
            i10 = i10 + 1
    return i10



def main():
    for x in range(0,numberOfAuthors):
        i10(x)


main()
