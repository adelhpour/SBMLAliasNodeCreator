from sbmlaliasnodecreator import SBMLAliasNodeCreator

input_sbml_file_name = "input_sbml_file_name.xml"
output_sbml_file_name = "output_sbml_file_name.xml"

sbanc = SBMLAliasNodeCreator()
sbanc.load(input_sbml_file_name)
sbanc.create_alias(targeted_species_glyphs=[{'S1': 3}])
sbanc.export(output_sbml_file_name)
