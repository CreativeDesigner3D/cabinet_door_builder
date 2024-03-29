import bpy
from . import types_cabinet_doors

class cabinet_door_builder_OT_create_door(bpy.types.Operator):
    bl_idname = "cabinet_door_builder.create_door"
    bl_label = "Create Door"
    bl_options = {'UNDO'}

    def execute(self, context):
        cdb_props = context.scene.cabinet_door_builder
        door = types_cabinet_doors.GeoNodeDoor()
        door.create("Door")
        door.set_input('Dim X',cdb_props.door_x_dim)
        door.set_input('Dim Y',cdb_props.door_y_dim)
        door.set_input('Outer Profile',cdb_props.get_outer_profile_object())
        door.set_input('Material',cdb_props.get_material())
        if cdb_props.include_inner_profile:
            door.set_input('Inner Profile',cdb_props.get_inner_profile_object())
            door.set_input('Panel Profile',cdb_props.get_panel_profile_object())
            door.set_input('Inset Amount',cdb_props.inset_amount)
        else:
            door.set_input('Inner Profile',None)
            door.set_input('Panel Profile',None)
            door.set_input('Inset Amount',.1)       
        return {'FINISHED'}
    

class cabinet_door_builder_OT_create_new_door(bpy.types.Operator):
    bl_idname = "cabinet_door_builder.create_new_door"
    bl_label = "Create New Door"
    bl_options = {'UNDO'}

    def execute(self, context):
        cdb_props = context.scene.cabinet_door_builder
        door = types_cabinet_doors.GeoNodeNewDoor()
        door.create("Door")
        door.set_input('Dim X',cdb_props.door_x_dim)
        door.set_input('Dim Y',cdb_props.door_y_dim)
        door.set_input('Outer Profile',cdb_props.get_outer_profile_object())
        if cdb_props.include_inner_profile:
            door.set_input('Inner Profile',cdb_props.get_inner_profile_object())
            door.set_input('Panel Profile',cdb_props.get_panel_profile_object())
            door.set_input('Inset Amount',cdb_props.inset_amount)
        else:
            door.set_input('Inner Profile',None)
            door.set_input('Panel Profile',None)
            door.set_input('Inset Amount',.1)       
        return {'FINISHED'}
    
classes = (
    cabinet_door_builder_OT_create_door,
    cabinet_door_builder_OT_create_new_door,
)

register, unregister = bpy.utils.register_classes_factory(classes)          