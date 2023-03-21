class SBMLAliasNodeCreator:

    def __init__(self):
        self.layout = None
        self.local_render = None

    def create_alias(self, model, targeted_species_glyphs=None, maximum_number_of_connected_nodes=0):
        self.extract_layout_render(model)
        if self.layout:
            highly_connected_species_glyphs = []
            if targeted_species_glyphs:
                highly_connected_species_glyphs = self.get_specified_highly_connected_species_glyphs(
                    targeted_species_glyphs)
            else:
                highly_connected_species_glyphs = self.get_all_highly_connected_species_glyphs(
                    maximum_number_of_connected_nodes)
            for highly_connected_species_glyph in highly_connected_species_glyphs:
                self.create_alias_species_glyphs(highly_connected_species_glyph)

    def extract_layout_render(self, model):
        # layout
        if model == None:
            raise SystemExit('Model does not exist.')
        layout_plugin = model.getPlugin('layout')
        if layout_plugin == None:
            raise SystemExit('This model does not contain layout info.')
        number_of_layouts = layout_plugin.getNumLayouts()
        if number_of_layouts:
            self.layout = layout_plugin.getLayout(0)

        # render
        render_plugin = self.layout.getPlugin("render")
        number_of_local_renders = render_plugin.getNumLocalRenderInformationObjects()
        if number_of_local_renders:
            self.local_render = render_plugin.getRenderInformation(0)

    def get_specified_highly_connected_species_glyphs(self, targeted_species_glyphs):
        highly_connected_species_glyphs = []
        for species_glyph in targeted_species_glyphs:
            species_glyph_id = list(species_glyph.keys())[0];
            connected_species_references = self.get_connected_species_references(species_glyph_id)
            if len(connected_species_references) > species_glyph[species_glyph_id]:
                highly_connected_species_glyphs.append({"id": species_glyph_id, "maximum_number_of_connected_nodes": species_glyph[species_glyph_id], "connected_species_references": connected_species_references})

        return highly_connected_species_glyphs

    def get_all_highly_connected_species_glyphs(self, maximum_number_of_connected_nodes):
        highly_connected_species_glyphs = []
        if maximum_number_of_connected_nodes > 0:
            for species_glyph_index in range(self.layout.getNumSpeciesGlyphs()):
                species_glyph_id = self.layout.getSpeciesGlyph(species_glyph_index).getId();
                connected_species_references = self.get_connected_species_references(species_glyph_id)
                if len(connected_species_references) > maximum_number_of_connected_nodes:
                    highly_connected_species_glyphs.append(
                        {"id": species_glyph_id, "maximum_number_of_connected_nodes": maximum_number_of_connected_nodes,
                         "connected_species_references": connected_species_references})

        return highly_connected_species_glyphs

    def get_connected_species_references(self, species_glyph_id):
        connected_species_references = []
        for reaction_glyph_index in range(self.layout.getNumReactionGlyphs()):
            reaction_glyph = self.layout.getReactionGlyph(reaction_glyph_index)
            for species_reference_glyph_index in range(reaction_glyph.getNumSpeciesReferenceGlyphs()):
                species_reference_glyph = reaction_glyph.getSpeciesReferenceGlyph(
                    species_reference_glyph_index)
                if species_reference_glyph.getSpeciesGlyphId() == species_glyph_id:
                    connected_species_references.append(species_reference_glyph)

        return connected_species_references

    @staticmethod
    def get_number_of_required_alias_species_glyphs(maximum_number_of_connected_species_reference_glyphs,
                                                    number_of_connected_species_references):
        number_of_required_alias_species_glyphs = len(
            number_of_connected_species_references) // maximum_number_of_connected_species_reference_glyphs
        if len(number_of_connected_species_references) % maximum_number_of_connected_species_reference_glyphs == 0:
            number_of_required_alias_species_glyphs -= 1
        return number_of_required_alias_species_glyphs

    def set_alias_species_glyph_mutual_features(self, alias_species_glyph, original_species_glyph, index_of_alias_species_glyph):
        alias_species_glyph.setSpeciesId(original_species_glyph.getSpeciesId())
        self.set_alias_graphical_object_bounding_box(alias_species_glyph, original_species_glyph.getBoundingBox(), index_of_alias_species_glyph)
        self.set_alias_graphical_object_style(alias_species_glyph, original_species_glyph)
        self.create_alias_species_glyph_text_glyphs(alias_species_glyph, original_species_glyph, index_of_alias_species_glyph)

    @staticmethod
    def set_alias_graphical_object_bounding_box(alias_graphical_object, bounding_box, index_of_graphical_object = 0):
        padding_x = 10.0 * index_of_graphical_object
        padding_y = 10.0 * index_of_graphical_object
        alias_graphical_object.getBoundingBox().setX(bounding_box.getX() + padding_x)
        alias_graphical_object.getBoundingBox().setY(bounding_box.getY() + padding_y)
        alias_graphical_object.getBoundingBox().setWidth(bounding_box.getWidth())
        alias_graphical_object.getBoundingBox().setHeight(bounding_box.getHeight())

    def set_alias_graphical_object_style(self, alias_graphical_object, original_graphical_object):
        if self.local_render:
            for local_style_index in range(self.local_render.getNumStyles()):
                local_style = self.local_render.getStyle(local_style_index)
                if local_style.getIdList().has_key(original_graphical_object.getId()):
                    local_style.addId(alias_graphical_object.getId())

    def create_alias_species_glyph_text_glyphs(self, alias_species_glyph, original_species_glyph, index_of_alias_species_glyph):
        for text_glyph_index in range(self.layout.getNumTextGlyphs()):
            original_text_glyph = self.layout.getTextGlyph(text_glyph_index)
            if original_text_glyph.getGraphicalObjectId() == original_species_glyph.getId():
                alias_text_glyph = self.layout.createTextGlyph()
                alias_text_glyph.setId(alias_species_glyph.getId() + "_text")
                alias_text_glyph.setGraphicalObjectId(alias_species_glyph.getId())
                self.set_alias_text_glyph_mutual_features(alias_text_glyph, original_text_glyph, index_of_alias_species_glyph)

    def set_alias_text_glyph_mutual_features(self, alias_text_glyph, original_text_glyph, index_of_alias_species_glyph):
        if original_text_glyph.isSetText():
            alias_text_glyph.setText(original_text_glyph.getText())
        self.set_alias_graphical_object_bounding_box(alias_text_glyph, original_text_glyph.getBoundingBox(), index_of_alias_species_glyph)
        self.set_alias_graphical_object_style(alias_text_glyph, original_text_glyph)

 
