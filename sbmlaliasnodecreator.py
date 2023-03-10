import libsbml


class SBMLAliasNodeCreator:

    def __init__(self):
        self.layout = None

    def create(self, model, maximum_number_of_connected_species_reference_glyphs):
        if maximum_number_of_connected_species_reference_glyphs > 0:
            self.extract_layout(model)
            if self.layout:
                highly_connected_species = self.get_highly_connected_species(maximum_number_of_connected_species_reference_glyphs)
                for species_info in highly_connected_species:
                    original_species_glyph = self.layout.getSpeciesGlyph(species_info["id"])
                    original_species_glyph.setId(species_info["id"] + "_0")
                    number_of_required_alias_species_glyphs = len(species_info["connected_species_references"]) // maximum_number_of_connected_species_reference_glyphs
                    for index_of_alias_species_glyphs in range(1, number_of_required_alias_species_glyphs):
                        alias_species_glyph = self.layout.createSpeciesGlyph()
                        alias_species_glyph.setId(species_info["id"] + "_" + str(index_of_alias_species_glyphs))
                        alias_species_glyph.setSpeciesId(original_species_glyph.getSpeciesId())
                        while len(species_info["connected_species_references"]) > (number_of_required_alias_species_glyphs - index_of_alias_species_glyphs) * maximum_number_of_connected_species_reference_glyphs:
                            connected_species_reference = species_info["connected_species_references"].pop()
                            connected_species_reference.setSpeciesGlyphId(alias_species_glyph.getId())

    def get_highly_connected_species(self, maximum_number_of_connected_species_reference_glyphs):
        highly_connected_species = []
        for species_glyph_index in range(self.layout.getNumSpeciesGlyphs()):
            connected_species_references = []
            species_glyph = self.layout.getSpeciesGlyph(species_glyph_index)
            number_of_connected_species_reference_glyphs = 0
            for reaction_glyph_index in range(self.layout.getNumReactionGlyphs()):
                reaction_glyph = self.layout.getReactionGlyph(reaction_glyph_index)
                for species_reference_glyph_index in range(reaction_glyph.getNumSpeciesReferenceGlyphs()):
                    species_reference_glyph = reaction_glyph.getSpeciesReferenceGlyph(
                        species_reference_glyph_index)
                    if species_reference_glyph.getSpeciesGlyphId() == species_glyph.getId():
                        connected_species_references.append(species_reference_glyph)
                        number_of_connected_species_reference_glyphs += 1
            if number_of_connected_species_reference_glyphs > maximum_number_of_connected_species_reference_glyphs:
                highly_connected_species.append({"id": species_glyph.getId(),
                                                 "connected_species_references": connected_species_references})

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



doc = libsbml.readSBMLFromFile("/Users/home/Downloads/Model1.xml")
SBMLAliasNodeCreator().create(doc.getModel(), 1)
libsbml.writeSBMLToFile(doc, "/Users/home/Downloads/Model2.xml")