from sbmlaliasnodecreator import SBMLAliasNodeCreator
import libsbml

sbml_string = "sbml_string_input"
maximum_number_of_connected_nodes = 4

sbanc = SBMLAliasNodeCreator()
sbanc.load(sbml_string)
sbanc.create_alias(maximum_number_of_connected_nodes)
sbml_string = sbanc.export()
