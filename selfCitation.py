from neo4jrestclient.client import GraphDatabase
import json
from py2neo import Graph, Node, Relationship, authenticate
import random
authenticate("52.35.21.1:7474","neo4j", "scibase")
graph=Graph("http://52.35.21.1:7474/db/data")
cypher = graph.cypher

numberOfAuthors = 100


def findSelfCitation(mainArticleList):
    articleList = []
    totalSelfCitation = 0
    for x in mainArticleList:
        query = 'MATCH (u:Article)<-[r:CITED_BY]-(m:Article) WHERE u.Name="%s" Return m.Name;'%x
        articles = cypher.execute(query)
        articleList = []
        for x in articles:
            a=x[0].encode("utf-8")
            articleList.append(a)
        intersectionSet = set(articleList).intersection(mainArticleList)
        totalSelfCitation = totalSelfCitation + len(intersectionSet);
    print(totalSelfCitation)
    return(totalSelfCitation)

def main():
    for y in range(0, numberOfAuthors):
        mainArticles = []
        totalSelfCitation = 0
        node = 'A'+str(y)
        query = 'MATCH (u:Author)-[r:AUTHORED_BY]->(m:Article) WHERE u.Name="%s" RETURN m.Name'%node
        articles = cypher.execute(query)
        for x in articles:
            a=x[0].encode("utf-8")
            mainArticles.append(a)
        totalSelfCitation = findSelfCitation(mainArticles)
        updateNode = 'MATCH (n:Author) where n.Name="%s"SET n.selfCitaion=%d;'%(node,totalSelfCitation)
        print(updateNode)
        cypher.execute(updateNode)

main()
