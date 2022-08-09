#Imported for the funtion urllib.parse.quote() used to quote particular characters in the URI
import urllib.parse as URLLParse

#Imported for the function csv.DictReader that allows to read a csv file as a dictionary
import csv

#Imported for the function os.getcwd() used to obtain the current working directory
import os

#Imported in order to count the time necessary to create the 5 starts data
import time

#Imported to write the triples
from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import RDF, RDFS

#Creating an URI from the object in question and the namespace we are using
def urify(namespace, UObject):
        UObject = UObject.lower().title().replace("-", "").replace("  ", "_").replace(" ","_").replace(".","")
        return namespace + URLLParse.quote(UObject)

#Getting the timestamp of when the porgram starts
start_time = time.time()

#Creating the ontology graph
g = Graph()

dbo = "http://dbpedia.org/ontology/"
dbr = "http://dbpedia.org/resource/"

#Creating namespaces and binding them to the knowledge graph
poifo = Namespace("http://poifinder.it/ontology/")
poifr = Namespace("http://poifinder.it/resoruce/")
g.bind("poifr", poifr)
g.bind("poifo", poifo)

#Creating a namespace in order to work with geographical coordinates
Geo = Namespace("https://www.w3.org/2003/01/geo/wgs84_pos#")

#Each dataset will be used individually

#Opening the 3 star dataset already cleaned called "Regione Sardegna - Luoghi di interesse turistico culturale.csv
with open(os.getcwd() + "/modified_files/" + "Regione Sardegna - Luoghi di interesse turistico culturale.csv") as sardegna:
    #Returning the dataset as a Dictionary we can access to
    sardegnaScan =csv.DictReader(sardegna)
    
    #Reading each row and creating a series of nodes out of it
    for row in sardegnaScan:
        
        #Extracting informations for any row and store them into temporary variables
        name = str(row["NOME"])
        location = str(row["COMUNE"]).lower().title()
        typology = str(row["MACRO TIPOLOGIA"])
        website = str(row["SCHEDA"])
        xCoord = row["DO_X"]
        yCoord = row["DO_Y"]
        
        #Creation of an unique URI
        #Example based on a entry of the overmentioned .csv file
        # http://poifinder/resource/Alghero/Base_Nautica_Usai_Srl
        CTISite = urify(poifr, location.lower().title() + "/" + name)
        
        g.add([URIRef(CTISite), RDF.type, poifo.POI])
        g.add([URIRef(CTISite), RDFS.label, Literal(name, lang="it")])
        g.add([URIRef(CTISite), poifo.Typology, Literal(typology, lang="it")])
        g.add([URIRef(CTISite), poifo.Link_to, Literal(website)])
        g.add([URIRef(CTISite), poifo.Is_located_in, URIRef(urify(dbr, location))])
        g.add([URIRef(CTISite), Geo.lat, Literal(yCoord)])
        g.add([URIRef(CTISite), Geo.long, Literal(xCoord)])

sardegna_time = time.time()
print("File \"Regione Sardegna - Luoghi di interesse turistico culturale.csv\" analyzed in" , sardegna_time - start_time, "seconds")

with open(os.getcwd() + "/modified_files/" + "Regione Puglia - Luoghi di interesse turistico culturale.csv") as puglia:
    #Returning the dataset as a Dictionary we can access to
    pugliaScan =csv.DictReader(puglia)
    
    #Reading each row and creating a series of nodes out of it
    for row in pugliaScan:
        
        #Extracting informations for any row and store them into temporary variables
        name = str(row["Nome attrattore"])
        location = str(row["Comune"]).lower().title()
        typology = str(row["Risorsa territoriale"])
        website = str(row["Sito WEB"])
        address = str(row["Indirizzo"] + ", " + row["Numero civico"])
        latitude = row["Latitudine"]
        longitude = row["Longitudine"]
        
        #Creation of an unique URI
        #Example based on a entry of the overmentioned .csv file
        # http://poifinder/resource/Accadia/Chiesa_Di_Santa_Maria_Maggiore_Di_Accadia
        CTISite = urify(poifr, location.lower().title() + "/" + name)
        
        g.add([URIRef(CTISite), RDF.type, poifo.POI])
        g.add([URIRef(CTISite), RDFS.label, Literal(name, lang="it")])
        g.add([URIRef(CTISite), poifo.Typology, Literal(typology, lang="it")])
        g.add([URIRef(CTISite), poifo.Link_to, Literal(website)])
        g.add([URIRef(CTISite), poifo.Is_located_in, URIRef(urify(dbr, location))])
        g.add([URIRef(CTISite), poifo.Address, Literal(address)])
        g.add([URIRef(CTISite), Geo.lat, Literal(latitude)])
        g.add([URIRef(CTISite), Geo.long, Literal(longitude)])

puglia_time = time.time()
print("File \"Regione Puglia - Luoghi di interesse turistico culturale.csv\" analyzed in" , puglia_time - sardegna_time, "seconds")

with open(os.getcwd() + "/modified_files/" + "Palermo - Luoghi di interesse turistico culturale.csv") as palermo:
    #Returning the dataset as a Dictionary we can access to
    palermoScan = csv.DictReader(palermo)
    
    #Reading each row and creating a series of nodes out of it
    for row in palermoScan:
        
        #Extracting informations for any row and store them into temporary variables
        name = str(row["Nome del sito"])
        typology = str(row["Tipo"]).lower().title()
        website = str(row["sito web"])
        address = str(row["indirizzo"])
        
        #Creation of an unique URI
        #Example based on the second entry of the overmentioned .csv file
        # http://poifinder/resource/Palermo/Cantieri_Culturali_Alla_Zisa
        CTISite = urify(poifr, "Palermo/" + name)
        
        g.add([URIRef(CTISite), RDF.type, poifo.POI])
        g.add([URIRef(CTISite), RDFS.label, Literal(name, lang="it")])
        g.add([URIRef(CTISite), poifo.Typology, Literal(typology, lang="it")])
        g.add([URIRef(CTISite), poifo.Link_to, Literal(website)])
        g.add([URIRef(CTISite), poifo.Is_located_in, URIRef(urify(dbo, "Palermo"))])
        g.add([URIRef(CTISite), poifo.Address, Literal(address)])

palermo_time = time.time()
print("File \"Palermo - Luoghi di interesse turistico culturale.csv\" analyzed in" , palermo_time - puglia_time, "seconds\n")
#Writing the knowledge graph on the file ~/result.ttl        
g.serialize(destination = str(os.getcwd() + "/result.ttl"), format="turtle")

end_time = time.time()
print("Knowledge graph serialized in", end_time - palermo_time, "seconds")