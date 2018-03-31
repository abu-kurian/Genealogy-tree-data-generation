from neo4jrestclient.client import GraphDatabase
import json
from py2neo import Graph, Node, Relationship, authenticate
import random
authenticate("52.35.21.1:7474","neo4j", "scibase")
graph=Graph("http://52.35.21.1:7474/db/data")
cypher = graph.cypher

numberOfAuthors = 100

def hIndex(x):
    citationList = []
    node = 'A'+str(x)
    print(node)
    findArticles = 'MATCH (u:Author)-[:AUTHORED_BY]->(m:Article) WHERE u.Name = "%s" RETURN m.Name'%node
    value = cypher.execute(findArticles)
    for x in value:
        a=x[0].encode("utf-8")
        findCitedArticles = 'MATCH (n:Article {Name:"%s"})<-[r:CITED_BY]-(m:Article) RETURN COUNT(r)'%(a)
        articles = cypher.execute(findCitedArticles)
        citationList.append(articles[0][0])
    citationList.sort(reverse=True)
    #print("list length is %d", len(citationList))
    hIndexValue = indexCalculation(citationList)
    print(hIndexValue)
    authorUpdate = 'MATCH (n:Author) where n.Name="%s"SET n.hIndex=%d;'%(node, hIndexValue)
    print(authorUpdate)
    cypher.execute(authorUpdate)

def indexCalculation(x):
    index = 0
    for j in range(0,len(x)):
        if(j+1>x[j]):
            break
        index = j+1
    return index



def main():
    for x in range(0,numberOfAuthors):
        print("calculating for %d",x)
        hIndex(x)


main()
