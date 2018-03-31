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

numberOfAuthors = 100
community = []

def calculateThreshold(node):
	genelogicalCitation = 0.0
	totalCitation = 0.0
	threshold = 0.0
	query = 'MATCH (u:Author) WHERE u.Name="%s" Return u.genelogicalCitation;'%node
   	genelogicalCitation = cypher.execute(query)
   	#print(type(genelogicalCitation[0][0]))
   	query = 'MATCH (u:Author) WHERE u.Name="%s" Return u.totalCitation;'%node
   	totalCitation = cypher.execute(query)
   	if(totalCitation[0][0]>0 and genelogicalCitation[0][0]<totalCitation[0][0]):
   	  threshold = genelogicalCitation[0][0]/float(totalCitation[0][0])
      print(genelogicalCitation[0][0])
      #print(genelogicalCitation[0][0])
      #print(totalCitation[0][0])
   	    #print((threshold))
   	updateNode = 'MATCH (n:Author) where n.Name="%s"SET n.communityCitation=%f;'%(node, threshold)
   	print(updateNode)
   	cypher.execute(updateNode)


def findCommunity(node):
	community = []
	articles = []
	nodeParents = []
	nodeSiblings = []
	articleList = []
	finalList = []
	query = 'MATCH (u:Author)-[r:PARENT_OF]->(m:Author) WHERE u.Name="%s" RETURN m.Name'%node
   	articles = cypher.execute(query)
   	for x in articles:
   	    a=x[0].encode("utf-8")
   	    nodeParents.append(a)
   	for parent in nodeParents:
   		query = 'MATCH (u:Author)-[r:PARENT_OF]->(m:Author) WHERE m.Name="%s" RETURN u.Name'%parent
   	   	articles = cypher.execute(query)
   	   	for x in articles:
   			a=x[0].encode("utf-8")
   	        nodeSiblings.append(a)
   	FindInstitute = 'MATCH (n:Author) Where n.Name="%s" RETURN n.Institute'%node
   	Domain = cypher.execute(FindInstitute)
   	query = 'MATCH (u:Author)-[r:AUTHORED_BY]->(m:Article) WHERE u.Name="%s" RETURN m.Name'%node
   	    #print(query)
   	articles = cypher.execute(query)
   	for j in articles:
   	    a=j[0].encode("utf-8")
   	    articleList.append(a)
   	    #print(articleList)
   	    for j in articleList:
   	        citationList = []
   	        query = 'MATCH (u:Article)<-[r:CITED_BY]-(m:Article) WHERE u.Name="%s" RETURN m.Name'%j
   	        citations = cypher.execute(query)
   	        for k in citations:
   	            a=k[0].encode("utf-8")
   	            citationList.append(a)
   	        for m in citationList:
   	        	query = 'MATCH (u:Author)-[r:AUTHORED_BY]->(m:Article) WHERE u.Name="%s" and u.Institute="%s" RETURN m.Name'%(m,Domain[0][0])
   	        	citations = cypher.execute(query)
   	        	for x in citations:
   	    			a=x[0].encode("utf-8")
   	    			community.append(a)
   	finalList = list(set(community+nodeSiblings))
   	return finalList

def mafiaCalc(siblingList, node):
	avgThreshold = 0;
	mafiaList = []
	citationCount  = 0
	mainNodeArticles = []
	otherNodeArticles = []
	otherNodeCitations = []
	FindThreshold = 'MATCH (n:Author) Where n.Name="%s" RETURN n.communityCitation'%node
	Domain = cypher.execute(FindThreshold)
	print(FindThreshold)
	nodeThreshold = int(Domain[0][0])
	print("current node threshold %f"%nodeThreshold)
	query = 'MATCH (u:Author)-[r:AUTHORED_BY]->(m:Article) WHERE u.Name="%s" RETURN m.Name'%node
	citations = cypher.execute(query)
        for x in citations:
        	a=x[0].encode("utf-8")
        	mainNodeArticles.append(a)
	for x in siblingList:
		FindThreshold = 'MATCH (n:Author) Where n.Name="%s" RETURN n.communityCitation'%x
    	Domain = cypher.execute(FindThreshold)
    	avgThreshold = int(Domain[0][0])
   	if(len(siblingList)==0):
		avgThreshold = 0
	else:
		avgThreshold = (avgThreshold+nodeThreshold)/(len(siblingList)+1)
	if avgThreshold>0:
		for j in siblingList:
			FindThreshold = 'MATCH (n:Author) Where n.Name="%s" RETURN n.communityCitation'%j
    		Domain = cypher.execute(FindThreshold)
    		Threshold = int(Domain[0][0])
    		if(Threshold/avgThreshold>1):
				mafiaList.append(j)
		for l in mafiaList:
			query = 'MATCH (u:Author)-[r:AUTHORED_BY]->(m:Article) WHERE u.Name="%s" RETURN m.Name'%l
			citations = cypher.execute(query)
			for x in citations:            
        			a=x[0].encode("utf-8")
        			otherNodeArticles.append(a)
        	for x in otherNodeArticles:
        		query = 'MATCH (u:Article)<-[r:CITED_BY]-(m:Article) WHERE u.Name="%s" RETURN m.Name'%j
            	citations = cypher.execute(query)
            	for k in citations:
                	a=k[0].encode("utf-8")
                	otherNodeCitations.append(a)
                for h in mainNodeArticles:
                	for i in otherNodeCitations:
                		if(h==i):
                			citationCount = citationCount + 1
  	else:
   		citationCount = 0;
   	updateNode = 'MATCH (n:Author) where n.Name="%s"SET n.communityCitation=%f;'%(node, citationCount)
   	cypher.execute(updateNode)
   	if(nodeThreshold>avgThreshold):
   		return nodeThreshold
   	else:
   		return 1



def main():
	CC = 0
	for i in range (0,numberOfAuthors):
		node = 'A'+str(i)
		print("calculting th for %s"%node)
		calculateThreshold(node)
	for i in range (0,numberOfAuthors):
		CC = 0
		siblingList = []
		node = 'A'+str(i)
		print("calculting cc for %s"%node)
		siblingList = findCommunity(node)
		CC = mafiaCalc(siblingList, node)
		updateNode = 'MATCH (n:Author) where n.Name="%s"SET n.NCC=%f;'%(node, 1-CC)
		#print(CC)
    	cypher.execute(updateNode)



main()