from neo4jrestclient.client import GraphDatabase
import json
from py2neo import Graph, Node, Relationship, authenticate
import random
#authenticate("52.35.21.1:7474","neo4j", "scibase")
#graph=Graph("http://52.35.21.1:7474/db/data")
#cypher = graph.cypher
authenticate("localhost:7474","neo4j", "kateisdog")
graph=Graph()
cypher = graph.cypher
numberOfAuthors = 1000

def findArticles(x):
    print("entered findArticles")
    articleList = []
    query = 'MATCH (u:Author)-[r:AUTHORED_BY]->(m:Article) WHERE u.Name="%s" RETURN m.Name'%x
    articles = cypher.execute(query)
    for x in articles:
        a=x[0].encode("utf-8")
        articleList.append(a)
    return articleList

def findTotalcount(x):
    totalCitations = 0
    for i in x:
        query = 'MATCH (u:Article)<-[r:CITED_BY]-(m:Article) WHERE u.Name="%s" Return COUNT(r);'%i
        numberOfCitations = cypher.execute(query)
        print(numberOfCitations[0][0])
        totalCitations = totalCitations + numberOfCitations[0][0]
    return(totalCitations)

def main():
    articleList = []
    for x in range(0,numberOfAuthors):
        mainNode = 'A'+str(x)
        print("*************")
        print("article processing - %s"%mainNode )
        articleList = findArticles(mainNode)
        print("number of elements %d",len(articleList))
        totalCitations = findTotalcount(articleList)
        updateNode = 'MATCH (n:Author) where n.Name="%s"SET n.totalCitation=%d;'%(mainNode, totalCitations)
        print(updateNode)
        cypher.execute(updateNode)

main()
