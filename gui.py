import bpy


from .op_create_manifest import get_separated_tags


class ANTEMPLATES_PT_templates_panel(bpy.types.Panel):
    bl_idname = "ANTEMPLATES_PT_templates_panel"
    bl_label = "Templates"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "Templates"


    @classmethod
    def poll(cls, context):
        if context.area.type == "NODE_EDITOR":
            if context.area.ui_type == "an_AnimationNodeTree":
                return True


    def draw(self, context):

        winman = context.window_manager
        properties_coll = winman.an_templates_properties

        layout = self.layout

        col = layout.column(align=True)

        row = col.row(align=True)
        row.prop(properties_coll, "nodetree_search", text="", icon='VIEWZOOM')
        row.prop(properties_coll, "nodetree_tag_search", text="", icon='STYLUS_PRESSURE')
        row.operator("antemplates.search_tag_menu_caller", text="", icon="COLLAPSEMENU")
        col.prop(properties_coll, "nodetree_categories_enum", text="", icon="FILE_FOLDER")
        col.template_list("ANTEMPLATES_UL_panel_ui_list", "", winman, "an_templates_nodetrees", properties_coll, "nodetrees_index", rows = 5)
        
        idx = winman.an_templates_properties.nodetrees_index

        row = layout.row(align=True)
        
        active_nodetree = None

        if idx in range(0, len(winman.an_templates_nodetrees)):
            active_nodetree = winman.an_templates_nodetrees[winman.an_templates_properties.nodetrees_index]

        row.operator("antemplates.import_nodetree", text="", icon="IMPORT")

        row.separator()

        row.label(text="", icon="URL")

        op1 = row.operator('antemplates.open_url', text="", icon='IMAGE')
        op2 = row.operator('antemplates.open_url', text="", icon='FILE_MOVIE')
        op3 = row.operator('antemplates.open_url', text="", icon='HELP')

        if active_nodetree is not None:
            op1.url = active_nodetree.image_preview_url
            op2.url = active_nodetree.video_preview_url
            op3.url = active_nodetree.readme_url


class ANTEMPLATES_PT_import_options_subpanel(bpy.types.Panel):
    bl_idname = "ANTEMPLATES_PT_import_options_subpanel"
    bl_label = "Import Options"
    bl_parent_id = "ANTEMPLATES_PT_templates_panel"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_options = {'DEFAULT_CLOSED'}


    def draw(self, context):

        winman = context.window_manager
        properties_coll = winman.an_templates_properties

        layout = self.layout

        # make it responsive TODO
        col = layout.column(align=True)
        col.prop(properties_coll, "import_original_scene")
        col.prop(properties_coll, "keep_original_objects")

        col2 = layout.column(align=True)
        if not properties_coll.import_original_scene and properties_coll.keep_original_objects:
            col2.enabled=True
        else:
            col2.enabled=False
        col2.prop(properties_coll, "original_objects_collection", text="")
        row = col2.row()
        if properties_coll.original_objects_collection != "SPECIFIC":
            row.enabled=False
        row.prop(properties_coll, "original_object_specific_collection", text="")


class ANTEMPLATES_PT_nodetree_infos_subpanel(bpy.types.Panel):
    bl_idname = "ANTEMPLATES_PT_nodetree_infos_subpanel"
    bl_label = "Nodetree Infos"
    bl_parent_id = "ANTEMPLATES_PT_templates_panel"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_options = {'DEFAULT_CLOSED'}


    def draw(self, context):

        winman = context.window_manager

        layout = self.layout
        
        idx = winman.an_templates_properties.nodetrees_index

        if idx in range(0, len(winman.an_templates_nodetrees)):
            active_nodetree = winman.an_templates_nodetrees[idx]
            
            col = layout.column(align=True)

            col.label(text=active_nodetree.description, icon="INFO")
            col.label(text=active_nodetree.blender_version, icon="BLENDER")
            col.label(text=active_nodetree.an_version, icon="ONIONSKIN_ON")
            col.label(text=active_nodetree.category, icon="FILE_FOLDER")
            #col.label(text=active_nodetree.hash, icon="RNA")
            #col.label(text=active_nodetree.file_url, icon="URL")
            
            col.label(text="Tags :", icon="VIEWZOOM")
            limit = 3
            ct = 0
            tag_reformat = ""
            for tag in get_separated_tags(active_nodetree.tags):
                tag_reformat += tag
                ct += 1
                if ct == limit:
                    col.label(text=tag_reformat)
                    tag_reformat = ""
                    ct = 0
                else:
                    tag_reformat += ", "
            if ct != 0:
                tag_reformat = tag_reformat[:-2]
                col.label(text=tag_reformat)


class ANTEMPLATES_PT_settings_panel(bpy.types.Panel):
    bl_idname = "ANTEMPLATES_PT_settings_panel"
    bl_label = "Settings"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "Templates"


    @classmethod
    def poll(cls, context):
        if context.area.type == "NODE_EDITOR":
            if context.area.ui_type == "an_AnimationNodeTree":
                return True


    def draw(self, context):

        layout = self.layout

        layout.operator("antemplates.refresh_templates", icon="FILE_REFRESH")
        layout.operator("antemplates.clear_downloads", icon="TRASH")