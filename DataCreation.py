from neo4jrestclient.client import GraphDatabase
import json
from py2neo import Graph, Node, Relationship, authenticate
import random
#authenticate("52.35.21.1:7474","neo4j", "scibase")
#graph=Graph("http://52.35.21.1:7474/db/data")
authenticate("localhost:7474","neo4j", "kateisdog")
graph=Graph()
cypher = graph.cypher
#cypher = graph.cypher




numberOfAuthors = 1000
numberOfArticles = 500
rangeOfRelationsAuthors = 100
rangeOfRelationsArticles = 100
rangeOfPublications = 100

domain=["Artificial Intelligence","Computational & Synthetic Biology","Computer Architecture","Computer Graphics, Vision, Animation, and Game Science","Computing for Development","Data Science","Data Management and Visualization","Human Computer Interaction","Machine Learning","Molecular Information Systems","Natural Language Processing","Programming Languages and Software Engineering","Security and Privacy","Systems and Networking","Theory of Computation","Ubiquitous Computing","Wireless and Sensor Systems"]
institute=['Boston University Graduate School','Massachusetts Institute of Technology','University of Notre Dame','Vrije Universiteit Amsterdam ', 'Rijksuniversiteit Groningen', 'Wesleyan University', 'University of California, Irvine ', 'University of Georgia ', 'University of California, Berkeley', 'University of California, San Diego', 'University of California, Los Angeles', 'Northwestern University', 'University of California, Berkeley  ', 'Washington University in St. Louis', ' The University of Chicago', 'Flinders University of South Australia', 'Washington University in St. Louis  ', ' University of California, Berkeley', 'University of California, Riverside', 'University Aix-Marseille', 'Massachusetts Institute of Technology ', 'University of Massachusetts Amhers ', 'University of Washington', 'University of Pittsburgh  ', 'The George Washington University', 'University of Rochester', 'Stanford University', 'Cornell University', 'Tel Aviv University', 'The University of Chicago', 'University of Auckland', 'University of New Brunswick', 'Pontificia Universidad Catlica de Chile', 'University of Iowa', 'Washington University in St. Louis', 'Indiana University', 'University of Toronto', 'Oregon State University', 'Aarhus University', 'University of Oxford', 'University of Arizona']
 
#domain=["Artificial Intelligence"]
#institute=['Boston University Graduate School']


def createNodesAuthor():
    for i in range(0,numberOfAuthors):
        print("created Author-%d"%i)
        x = 'A'+str(i)
        graph.create(Node("Author",Name=x, Domain=domain[random.randrange(0,len(domain))], Institute=institute[random.randrange(0,len(institute))], totalCitation=0, genelogicalCitation=0, communityCitation=0, selfCitaion=0, hIndex=0, i10=0, NGC=0, NCC = 0, OCQ = 0))
        #graph.create(Node("Author",Name=x, Domain="Computational & Synthetic Biology", totalCitation=0, genelogicalCitation=0, communityCitation=0, selfCitaion=0, hIndex=0, i10=0))
    return

def createNodesArticle():
    for i in range(0,numberOfArticles):
        print("created Article-%d"%i)
        x = 'AR'+str(i)
        graph.create(Node("Article",Name=x, Domain=domain[random.randrange(0,len(domain))]))
    return

def createRelationAuthor(x):
    print("creating author relation %d"%x)
    mainNode = 'A'+str(x)
    FindDomainMain = 'MATCH (n:Author) Where n.Name="%s" RETURN n.Domain'%mainNode
    MainDomain = cypher.execute(FindDomainMain)
    numberOfRelations =  random.randrange(0, rangeOfRelationsAuthors)
    for i in range(0, numberOfRelations):
        otherNodeValue = random.randrange(0, x-1)
        otherNode ='A'+str(otherNodeValue)
        FindDomainOther = 'MATCH (n:Author) Where n.Name="%s" RETURN n.Domain'%otherNode
        otherDomain = cypher.execute(FindDomainOther)
        if(MainDomain[0][0]==otherDomain[0][0]):
            checkRelation = 'MATCH (n:Author {Name:"%s"})-[r:PARENT_OF]-(m:Author {Name:"%s"}) RETURN SIGN(COUNT(r))'%(mainNode, otherNode)
            value = cypher.execute(checkRelation)
            if(value[0][0]==0):
                query = "MATCH (a:Author),(b:Author) WHERE a.Name='%s' AND b.Name='%s' CREATE (a)-[r:PARENT_OF]->(b)"%(mainNode,otherNode)
                cypher.execute(query)

def createRelationArticle(x):
    print("creating article relation %d"%x)
    mainNode = 'AR'+str(x)
    FindDomainMain = 'MATCH (n:Article) Where n.Name="%s" RETURN n.Domain'%mainNode
    MainDomain = cypher.execute(FindDomainMain)
    numberOfRelations =  random.randrange(0, rangeOfRelationsArticles)
    for i in range(0, numberOfRelations):
        otherNodeValue = random.randrange(0, x-1)
        otherNode ='AR'+str(otherNodeValue)
        FindDomainOther = 'MATCH (n:Article) Where n.Name="%s" RETURN n.Domain'%otherNode
        otherDomain = cypher.execute(FindDomainOther)
        if(MainDomain[0][0]==otherDomain[0][0]):
            checkRelation = 'MATCH (n:Article {Name:"%s"})-[r:CITED_BY]-(m:Article {Name:"%s"}) RETURN SIGN(COUNT(r))'%(mainNode, otherNode)
            value = cypher.execute(checkRelation)
            if(mainNode!=otherNode and value[0][0]==0):
                query = "MATCH (a:Article),(b:Article) WHERE a.Name='%s' AND b.Name='%s' CREATE (a)-[r:CITED_BY]->(b)"%(mainNode,otherNode)
                cypher.execute(query)

# def authorArticleRelation(x):
#     print("creating article author relation %d"%x)
#     mainNode = 'A'+str(x)
#     FindDomainMain = 'MATCH (n:Author) Where n.Name="%s" RETURN n.Domain'%mainNode
#     MainDomain = cypher.execute(FindDomainMain)
#     numberOfRelations =  random.randrange(1, rangeOfPublications)
#     count = 0
#     while count<=1:
#         for i in range(0, numberOfRelations):
#             otherNodeValue = random.randrange(0, numberOfArticles)
#             otherNode ='AR'+str(otherNodeValue)
#             FindDomainOther = 'MATCH (n:Article) Where n.Name="%s" RETURN n.Domain'%otherNode
#             otherDomain = cypher.execute(FindDomainOther)
#             if(MainDomain[0][0]==otherDomain[0][0]):
#                 checkRelation = 'MATCH (n:Author {Name:"%s"})-[r:AUTHORED_BY]-(m:Article {Name:"%s"}) RETURN SIGN(COUNT(r))'%(mainNode, otherNode)
#                 value = cypher.execute(checkRelation)
#                 if(value[0][0]==0):
#                     count=count+1
#                     query = "MATCH (a:Author),(b:Article) WHERE a.Name='%s' AND b.Name='%s' CREATE (a)-[r:AUTHORED_BY]->(b)"%(mainNode,otherNode)
#                     cypher.execute(query)

def articleAuthorRelation(x):
    print("creating article author relation %d"%x)
    mainNode = 'AR'+str(x)
    FindDomainMain = 'MATCH (n:Article) Where n.Name="%s" RETURN n.Domain'%mainNode
    MainDomain = cypher.execute(FindDomainMain)
    numberOfRelations =  random.randrange(1, rangeOfPublications)
    count = 0
    while count<1:
        print("here %s"%mainNode)
        for i in range(0, numberOfRelations):
            otherNodeValue = random.randrange(0, numberOfAuthors)
            otherNode ='A'+str(otherNodeValue)
            FindDomainOther = 'MATCH (n:Author) Where n.Name="%s" RETURN n.Domain'%otherNode
            otherDomain = cypher.execute(FindDomainOther)
            if(MainDomain[0][0]==otherDomain[0][0]):
                checkRelation = 'MATCH (n:Author {Name:"%s"})-[r:AUTHORED_BY]-(m:Article {Name:"%s"}) RETURN SIGN(COUNT(r))'%(otherNode, mainNode)
                value = cypher.execute(checkRelation)
                if(value[0][0]==0):
                    count=count+1
                    query = "MATCH (a:Author),(b:Article) WHERE a.Name='%s' AND b.Name='%s' CREATE (a)-[r:AUTHORED_BY]->(b)"%(otherNode, mainNode)
                    cypher.execute(query)



def main():
    createNodesAuthor()
    createNodesArticle()
    for x in range(2, numberOfAuthors):
        createRelationAuthor(x)
    for x in range(2, numberOfArticles):
        createRelationArticle(x)
    # for x in range(0, numberOfAuthors):
    #     authorArticleRelation(x)
    for x in range(0, numberOfArticles):
        articleAuthorRelation(x)




main()
