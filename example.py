doc = libsbml.readSBMLFromFile("/Users/home/Downloads/Model3.xml")
SBMLAliasNodeCreator().create(doc.getModel(), 1)
libsbml.writeSBMLToFile(doc, "/Users/home/Downloads/Model4.xml")