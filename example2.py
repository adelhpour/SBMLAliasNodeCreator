from sbmlaliasnodecreator import SBMLAliasNodeCreator

input_sbml_file_name = "input_sbml_file_name.xml"
output_sbml_file_name = "output_sbml_file_name.xml"

sbanc = SBMLAliasNodeCreator()
sbanc.load(input_sbml_file_name)
sbanc.create_alias(maximum_number_of_connected_nodes=4)
sbanc.export(output_sbml_file_name)
