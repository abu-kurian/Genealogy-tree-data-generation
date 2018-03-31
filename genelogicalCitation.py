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

numberOfAuthors = 10

def findRelatedNodesUp(node):
    citationCount = 0
    nodeListUp = []
    print("entered node up")
    checkRelation = 'MATCH (u:Author)<-[r:PARENT_OF]-(m:Author) WHERE m.Name="%s" RETURN u.Name'%node
    relations = cypher.execute(checkRelation)
    #print(checkRelation)
    #print(len(relations))
    #if(len(relations)==0):
    for x in relations:
        a=x[0].encode("utf-8")
        nodeListUp.append(a)
	#print("x is");
	#print(x)
	#print(len(nodeListUp))
    for y in range(0,len(nodeListUp)):
        checkRelation = 'MATCH (u:Author)<-[r:PARENT_OF]-(m:Author) WHERE m.Name="%s" RETURN u.Name'%nodeListUp[y]
        relations = cypher.execute(checkRelation)
        for j in relations:
            a=j[0].encode("utf-8")
            nodeListUp.append(a)
    #print("relations up")
    #print(nodeListUp)
    #print(list(set(nodeListUp)))
    return list(set(nodeListUp))


def findRelatedNodesDown(node):
	nodeListDown = []
	count = 0
	print("entered node down")
	checkRelation = 'MATCH (u:Author)<-[r:PARENT_OF]-(m:Author) WHERE u.Name="%s" RETURN m.Name'%node
	relations = cypher.execute(checkRelation)
	#print(checkRelation)
   	for x in relations:
   	    a=x[0].encode("utf-8")
   	    nodeListDown.append(a)
   	#print(len(nodeListDown))
   	for y in range(0,len(nodeListDown)):
   	    checkRelation = 'MATCH (u:Author)<-[r:PARENT_OF]-(m:Author) WHERE u.Name="%s" RETURN m.Name'%nodeListDown[y]
   	    relations = cypher.execute(checkRelation)
   	    count = count + 1
   	    #print(count)
   	    #print(len(relations))
   	    for j in relations:
   	    	#print(j)
   	        a=j[0].encode("utf-8")
   	        #print(a)
   	        nodeListDown.append(a)
   	print("final list")
   	print(len(nodeListDown))
    #print("relations down")
    #print(nodeListDown)
    #print(list(set(nodeListDown)))
    #print(nodeListDown)
   	return list(set(nodeListDown))

def citationCount(x, mainArticles ):
    articleList = []
    citationList = []
    intersectionSet = []
    totalCitations = 0
    count = 0
    print("entered citation count")
    for author in range(0,len(x)):
        query = 'MATCH (u:Author)-[r:AUTHORED_BY]->(m:Article) WHERE u.Name="%s" RETURN m.Name'%x[author]
        #print(query)
        articles = cypher.execute(query)
        #print(len(articles))
        for j in range(0,len(articles)):
            a=articles[j][0].encode("utf-8")
            articleList.append(a)
            #count = count + 1
            #print(count)
        #print(articleList)
        for j in range(0,len(articleList)):
            citationList = []
            query = 'MATCH (u:Article)<-[r:CITED_BY]-(m:Article) WHERE u.Name="%s" RETURN m.Name'%articleList[j]
            #print(query)
            citations = cypher.execute(query)
            for k in range(0,len(citations)):
                a=citations[k][0].encode("utf-8")
                citationList.append(a)
            intersectionSet = set(citationList).intersection(mainArticles)
            #print("main articles")
            #print(mainArticles)
            #print("intersection")
            #print(intersectionSet)
        totalCitations = totalCitations + len(intersectionSet)
    print(totalCitations)
    return totalCitations

def main():
    mainArticles = []
    nodeListUp = []
    nodeListDown = []
    genelogicalCitation = 0
    for i in range(1, numberOfAuthors):
        print("**************************")
        print("finding for %d  "%i)
        genelogicalCitation = 0
        mainArticles = []
        nodeListUp = []
        nodeListDown = []
        node = 'A'+str(i)
        query = 'MATCH (u:Author)-[r:AUTHORED_BY]->(m:Article) WHERE u.Name="%s" RETURN m.Name'%node
        #print(query)
        articles = cypher.execute(query)
        for x in articles:
            a=x[0].encode("utf-8")
            mainArticles.append(a)
        #print("node up")
        nodeListUp = findRelatedNodesUp(node)
        #print("node down")
        nodeListDown = findRelatedNodesDown(node)
        genelogicalCitation = citationCount(nodeListDown, mainArticles )
        genelogicalCitation = genelogicalCitation + citationCount(nodeListUp, mainArticles )
        updateNode = 'MATCH (n:Author) where n.Name="%s"SET n.genelogicalCitation=%d;'%(node, genelogicalCitation)
        print(updateNode)
        cypher.execute(updateNode)

        #print(list(set(nodeListDown)))
        #print(list(set(nodeListUp)))

main()
