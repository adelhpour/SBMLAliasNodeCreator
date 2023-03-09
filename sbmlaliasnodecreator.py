import libsbml as sbml


class CreateAliasNode:

    def __init__(self, model, maximum_number_of_connected_species_reference_glyphs):
        self.layout = None
        self.create(model, maximum_number_of_connected_species_reference_glyphs)

    def create(self, model, maximum_number_of_connected_species_reference_glyphs):
        self.extract_layout(model)
        if self.layout:
            highly_connected_species = self.get_highly_connected_species(maximum_number_of_connected_species_reference_glyphs)

    def get_highly_connected_species(self, maximum_number_of_connected_species_reference_glyphs):
        highly_connected_species = []
        for species_glyph_index in range(self.layout.getNumSpeciesGlyphs()):
            species_glyph = self.layout.getSpeciesGlyph(species_glyph_index)
            number_of_connected_species_reference_glyphs = 0
            for reaction_glyph_index in range(self.layout.getNumReactionGlyphs()):
                reaction_glyph = self.layout.getReactionGlyph(reaction_glyph_index)
                for species_reference_glyph_index in range(reaction_glyph.getNumSpeciesReferenceGlyphs()):
                    species_reference_glyph = reaction_glyph.getSpeciesReferenceGlyph(
                        species_reference_glyph_index)
                    if species_reference_glyph.getSpeciesGlyphId() == species_glyph.getId():
                        number_of_connected_species_reference_glyphs += 1
            if number_of_connected_species_reference_glyphs > maximum_number_of_connected_species_reference_glyphs:
                highly_connected_species.append({species_glyph.getId(), number_of_connected_species_reference_glyphs})

        return highly_connected_species

    def extract_layout(self, model):
        self.check(model, "get model")
        layout_plugin = model.getPlugin('layout')
        self.check(layout_plugin, "get layout plugin")
        number_of_layouts = layout_plugin.getNumLayouts()
        if number_of_layouts:
             self.layout = layout_plugin.getLayout(0)


    def check(self, value, message):
        if value == None:
            raise SystemExit('LibSBML returned a null value trying to ' + message + '.')
        elif type(value) is int:
            if value == libsbml.LIBSBML_OPERATION_SUCCESS:
                return
            else:
                err_msg = 'Error encountered trying to ' + message + '.' \
                          + 'LibSBML returned error code ' + str(value) + ': "' \
                          + OperationReturnValue_toString(value).strip() + '"'
                raise SystemExit(err_msg)
        else:
            return



doc = sbml.readSBMLFromFile("/Users/home/Downloads/Model1.xml")
CreateAliasNode(doc.getModel(), 1)