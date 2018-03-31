from neo4jrestclient.client import GraphDatabase
import json
from py2neo import Graph, Node, Relationship, authenticate
import random
authenticate("52.35.21.1:7474","neo4j", "scibase")
graph=Graph("http://52.35.21.1:7474/db/data")
cypher = graph.cypher


# domain=["Artificial Intelligence","Computational & Synthetic Biology","Computer Architecture","Computer Graphics, Vision, Animation, and Game Science","Computing for Development","Data Science","Data Management and Visualization","Human Computer Interaction","Machine Learning","Molecular Information Systems","Natural Language Processing","Programming Languages and Software Engineering","Security and Privacy","Systems and Networking","Theory of Computation","Ubiquitous Computing","Wireless and Sensor Systems"]
domain=["Artificial Intelligence","Computational & Synthetic Biology"]


def calculateThreshold(domain):
    genelogicalCitation = 0
    totalCitation = 0
    threshold = 0.0
    query = 'MATCH (u:Author) WHERE u.Domain="%s" Return u.Name;'%domain
    authors = cypher.execute(query)
    for x in authors:
        author = x[0].encode("utf-8")
        query = 'MATCH (u:Author) WHERE u.Name="%s" Return u.genelogicalCitation;'%author
        genelogicalCitation = cypher.execute(query)
        query = 'MATCH (u:Author) WHERE u.Name="%s" Return u.totalCitation;'%author
        totalCitation = cypher.execute(query)
        if(totalCitation[0][0]>0):
            threshold = genelogicalCitation[0][0]/float(totalCitation[0][0])
        updateNode = 'MATCH (n:Author) where n.Name="%s"SET n.communityCitation=%f;'%(author, threshold)
        cypher.execute(updateNode)

def corruptAuthor(domain):
    totalThreshold = 0
    query = 'MATCH (u:Author) WHERE u.Domain="%s" Return u.Name;'%domain
    authors = cypher.execute(query)
    query = 'MATCH (u:Author) WHERE u.Domain="%s" Return COUNT(u.Name);'%domain
    numberOfAuthors = cypher.execute(query)
    for x in authors:
        author = x[0].encode("utf-8")
        query = 'MATCH (u:Author) WHERE u.Name="%s" Return u.communityCitation;'%author
        communityCitation = cypher.execute(query)
        totalThreshold = totalThreshold + communityCitation[0][0]
    thresholdAvg = totalThreshold/numberOfAuthors[0][0]
    print(thresholdAvg)
    for x in authors:
        author = x[0].encode("utf-8")
        query = 'MATCH (u:Author) WHERE u.Name="%s" Return u.communityCitation;'%author
        communityCitation = cypher.execute(query)
        newCommunityCitation = communityCitation[0][0]/thresholdAvg
        updateNode = 'MATCH (n:Author) where n.Name="%s"SET n.communityCitation=%f;'%(author, newCommunityCitation)
        cypher.execute(updateNode)


def main():
    for x in domain:
        print("for domain %s"%x)
        calculateThreshold(x)
        corruptAuthor(x)


main()
