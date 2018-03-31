rom neo4jrestclient.client import GraphDatabase
import json
from py2neo import Graph, Node, Relationship, authenticate
import random
authenticate("52.35.21.1:7474","neo4j", "scibase")
graph=Graph("http://52.35.21.1:7474/db/data")
cypher = graph.cypher

numberOfAuthors = 100

def findRelatedNodesUp(node):
    citationCount = 0
    nodeListUp = []
    checkRelation = 'MATCH (u:Author)<-[r:PARENT_OF]-(m:Author) WHERE m.Name="%s" RETURN u.Name'%node
    relations = cypher.execute(checkRelation)
    #print(checkRelation)
    print(len(relations))
    #if(len(relations)==0):
    for x in relations:
        a=x[0].encode("utf-8")
        nodeListUp.append(a)
	#print("x is");
	#print(x)
    for x in nodeListUp:
        checkRelation = 'MATCH (u:Author)<-[r:PARENT_OF]-(m:Author) WHERE m.Name="%s" RETURN u.Name'%x
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
    checkRelation = 'MATCH (u:Author)<-[r:PARENT_OF]-(m:Author) WHERE u.Name="%s" RETURN m.Name'%node
    relations = cypher.execute(checkRelation)
    for x in relations:
        a=x[0].encode("utf-8")
        nodeListDown.append(a)
    for x in nodeListDown:
        checkRelation = 'MATCH (u:Author)<-[r:PARENT_OF]-(m:Author) WHERE u.Name="%s" RETURN m.Name'%x
        relations = cypher.execute(checkRelation)
        for j in relations:
            a=j[0].encode("utf-8")
            nodeListDown.append(a)
    #print("relations down")
    #print(nodeListDown)
    #print(list(set(nodeListDown)))
    return list(set(nodeListDown))


def genDecimalValue(nodeList, node):
    genelogicalCitation = 0
    totalCitation = 0
    totalValue = 0
    GC = 0
    for x in nodeList:
        query = 'MATCH (u:Author) WHERE u.Name="%s" Return u.genelogicalCitation;'%x
        genelogicalCitation = cypher.execute(query)
        query = 'MATCH (u:Author) WHERE u.Name="%s" Return u.totalCitation;'%x
        totalCitation = cypher.execute(query)
        if(totalCitation[0][0]>0):
            threshold = genelogicalCitation[0][0]/float(totalCitation[0][0])
        else
            threshold = 0
        totalValue = totalValue + threshold
    query = 'MATCH (u:Author) WHERE u.Name="%s" Return u.genelogicalCitation;'%node
    genelogicalCitation = cypher.execute(query)
    query = 'MATCH (u:Author) WHERE u.Name="%s" Return u.totalCitation;'%node
    totalCitation = cypher.execute(query)
    if(totalCitation[0][0]>0):
        threshold = genelogicalCitation[0][0]/float(totalCitation[0][0])
    else
        threshold = 0
    totalValue = totalValue + threshold;
    GC = totalValue/(len(nodeList)+1)
    return GC;




def main():
    mainArticles = []
    nodeListUp = []
    nodeListDown = []
    genelogicalCitation = 0
    nodeListFull = []
    for i in range(1, numberOfAuthors):
        print("**************************")
        print("finding for %d  "%i)
        genelogicalCitation = 0
        mainArticles = []
        nodeListUp = []
        nodeListDown = []
        node = 'A'+str(i)
        query = 'MATCH (u:Author)-[r:AUTHORED_BY]->(m:Article) WHERE u.Name="%s" RETURN m.Name'%node
        articles = cypher.execute(query)
        for x in articles:
            a=x[0].encode("utf-8")
            mainArticles.append(a)
        nodeListUp = findRelatedNodesUp(node)
        nodeListDown = findRelatedNodesDown(node)
        #genelogicalCitation = citationCount(nodeListDown, mainArticles )
        #genelogicalCitation = genelogicalCitation + citationCount(nodeListUp, mainArticles )
        nodeListFull = list(set(nodeListUp+nodeListDown))
        genelogicalCitation = genDecimalValue(nodeListFull, node) 
        updateNode = 'MATCH (n:Author) where n.Name="%s"SET n.NGC=%d;'%(node, 1-genelogicalCitation)
        print(updateNode)
        cypher.execute(updateNode)

        #print(list(set(nodeListDown)))
        #print(list(set(nodeListUp)))

main()
