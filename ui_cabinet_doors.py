import bpy

class CABINET_DOOR_BUILDER_PT_library(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_label = "Cabinet Door Builder"
    bl_category = "Library"    

    def draw(self, context):
        layout = self.layout

        cdb_props = context.scene.cabinet_door_builder
        
        row = layout.row()
        row.prop(cdb_props,'door_tabs',expand=True)
        
        if cdb_props.door_tabs == 'Current Door':
            layout.prop(cdb_props,'door_x_dim')
            layout.prop(cdb_props,'door_y_dim')
            layout.prop(cdb_props,'material')
            layout.prop(cdb_props,'outer_profile')
            layout.prop(cdb_props,'include_inner_profile')
            if cdb_props.include_inner_profile:
                layout.prop(cdb_props,'inner_profile')
                layout.prop(cdb_props,'panel_profile')
                layout.prop(cdb_props,'inset_amount')

            layout.operator('cabinet_door_builder.create_door')
        else:
            layout.prop(cdb_props,'door_x_dim')
            layout.prop(cdb_props,'door_y_dim')
            layout.prop(cdb_props,'door_shape')
            if cdb_props.joinery_type == 'Mitered' and cdb_props.door_shape not in {'Slab','Square'}:
                layout.label(text="Only Square Shape Available for Mitered")
            layout.prop(cdb_props,'outer_profile')
            if cdb_props.door_shape != 'Slab':
                layout.prop(cdb_props,'joinery_type')
                layout.prop(cdb_props,'panel_type')
                layout.prop(cdb_props,'inner_profile')
                if cdb_props.panel_type == 'Raised Panel':
                    layout.prop(cdb_props,'panel_profile')
                else:
                    layout.prop(cdb_props,'change_inset_panel_material')
                    if cdb_props.change_inset_panel_material:
                        layout.prop(cdb_props,'panel_material')

                row = layout.row()
                row.label(text="Stile Width")
                row.prop(cdb_props,'left_stile_width',text='Left')
                row.prop(cdb_props,'right_stile_width',text='Right')
                row = layout.row()
                row.label(text="Rail Width")                
                row.prop(cdb_props,'top_rail_width',text="Top")
                row.prop(cdb_props,'bottom_rail_width',text='Bottom')

            layout.operator('cabinet_door_builder.create_new_door')

classes = (
    CABINET_DOOR_BUILDER_PT_library,
)

register, unregister = bpy.utils.register_classes_factory(classes)        