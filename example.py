import libsbml
from sbmlaliasnodecreator import SBMLAliasNodeCreator

maximum_number_of_connected_nodes = 4
doc = libsbml.readSBMLFromFile("example.xml")
SBMLAliasNodeCreator().create(doc.getModel(), maximum_number_of_connected_nodes)
libsbml.writeSBMLToFile(doc, "example.xml")