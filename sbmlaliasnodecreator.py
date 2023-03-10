import libsbml


class SBMLAliasNodeCreator:

    def __init__(self):
        self.layout = None
        self.local_render = None

    def create(self, model, maximum_number_of_connected_species_reference_glyphs):
        if maximum_number_of_connected_species_reference_glyphs > 0:
            self.extract_layout_render(model)
            if self.layout:
                list_of_highly_connected_species = self.get_highly_connected_species_glyphs(maximum_number_of_connected_species_reference_glyphs)
                for highly_connected_species in list_of_highly_connected_species:
                    self.create_alias_species_glyphs(maximum_number_of_connected_species_reference_glyphs, highly_connected_species)

    def extract_layout_render(self, model):
        #layout
        self.check(model, "get model")
        layout_plugin = model.getPlugin('layout')
        self.check(layout_plugin, "get layout plugin")
        number_of_layouts = layout_plugin.getNumLayouts()
        if number_of_layouts:
             self.layout = layout_plugin.getLayout(0)

        #render
        render_plugin = self.layout.getPlugin("render")
        self.check(render_plugin, "get render plugin")
        number_of_local_renders = render_plugin.getNumLocalRenderInformationObjects()
        if number_of_local_renders:
            self.local_render = render_plugin.getRenderInformation(0)

    @staticmethod
    def check(value, message):
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

    def get_highly_connected_species_glyphs(self, maximum_number_of_connected_species_reference_glyphs):
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

    def create_alias_species_glyphs(self, maximum_number_of_connected_species_reference_glyphs, species_info):
        original_species_glyph = self.layout.getSpeciesGlyph(species_info["id"])
        number_of_required_alias_species_glyphs = self.get_number_of_required_alias_species_glyphs(
            maximum_number_of_connected_species_reference_glyphs, species_info["connected_species_references"])
        for index_of_alias_species_glyphs in range(1, number_of_required_alias_species_glyphs + 1):
            alias_species_glyph = self.layout.createSpeciesGlyph()
            alias_species_glyph.setId(species_info["id"] + "_" + str(index_of_alias_species_glyphs))
            self.set_alias_species_glyph_mutual_features(alias_species_glyph, original_species_glyph)
            while len(species_info["connected_species_references"]) > (
                    number_of_required_alias_species_glyphs - index_of_alias_species_glyphs + 1) * maximum_number_of_connected_species_reference_glyphs:
                connected_species_reference = species_info["connected_species_references"].pop()
                connected_species_reference.setSpeciesGlyphId(alias_species_glyph.getId())

    @staticmethod
    def get_number_of_required_alias_species_glyphs(maximum_number_of_connected_species_reference_glyphs,
                                                    number_of_connected_species_references):
        number_of_required_alias_species_glyphs = len(
            number_of_connected_species_references) // maximum_number_of_connected_species_reference_glyphs
        if len(number_of_connected_species_references) % maximum_number_of_connected_species_reference_glyphs == 0:
            number_of_required_alias_species_glyphs -= 1
        return number_of_required_alias_species_glyphs
    def set_alias_species_glyph_mutual_features(self, alias_species_glyph, original_species_glyph):
        alias_species_glyph.setSpeciesId(original_species_glyph.getSpeciesId())
        self.set_alias_graphical_object_bounding_box(alias_species_glyph, original_species_glyph.getBoundingBox())
        self.create_text_glyphs_of_alias_species_glyph(alias_species_glyph, original_species_glyph)

    @staticmethod
    def set_alias_graphical_object_bounding_box(alias_graphical_object, bounding_box):
        alias_graphical_object.getBoundingBox().setX(bounding_box.getX())
        alias_graphical_object.getBoundingBox().setY(bounding_box.getY())
        alias_graphical_object.getBoundingBox().setWidth(bounding_box.getWidth())
        alias_graphical_object.getBoundingBox().setHeight(bounding_box.getHeight())

    def create_text_glyphs_of_alias_species_glyph(self, alias_species_glyph, original_species_glyph):
        for text_glyph_index in range(self.layout.getNumTextGlyphs()):
            original_text_glyph = self.layout.getTextGlyph(text_glyph_index)
            if original_text_glyph.getGraphicalObjectId() == original_species_glyph.getId():
                alias_text_glyph = self.layout.createTextGlyph()
                alias_text_glyph.setId(alias_species_glyph.getId() + "_text")
                alias_text_glyph.setGraphicalObjectId(alias_species_glyph.getId())
                self.set_alias_text_glyph_mutual_features(alias_text_glyph, original_text_glyph)

    def set_alias_text_glyph_mutual_features(self, alias_text_glyph, original_text_glyph):
        if original_text_glyph.isSetText():
            alias_text_glyph.setText(original_text_glyph.getText())
        self.set_alias_graphical_object_bounding_box(alias_text_glyph, original_text_glyph.getBoundingBox())







doc = libsbml.readSBMLFromFile("/Users/home/Downloads/Model3.xml")
SBMLAliasNodeCreator().create(doc.getModel(), 1)
libsbml.writeSBMLToFile(doc, "/Users/home/Downloads/Model4.xml")