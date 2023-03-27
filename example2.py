from sbmlaliasnodecreator import SBMLAliasNodeCreator

input_sbml_file_name = "input_sbml_file_name.xml"
output_sbml_file_name = "output_sbml_file_name.xml"
maximum_number_of_connected_nodes = 4

sbanc = SBMLAliasNodeCreator()
sbanc.load(input_sbml_file_name=input_sbml_file_name)
sbanc.create_alias(maximum_number_of_connected_nodes=maximum_number_of_connected_nodes)
sbanc.export(output_sbml_file_name)
