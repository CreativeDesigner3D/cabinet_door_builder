import bpy
import os
from bpy.types import (
        Operator,
        Panel,
        PropertyGroup,
        UIList,
        AddonPreferences,
        )
from bpy.props import (
        BoolProperty,
        FloatProperty,
        IntProperty,
        PointerProperty,
        StringProperty,
        CollectionProperty,
        EnumProperty,
        )

OUTER_PROFILE_PATH = os.path.join(os.path.dirname(__file__),'Door Profiles','Outer Profiles')
INNER_PROFILE_PATH = os.path.join(os.path.dirname(__file__),'Door Profiles','Inner Profiles')
PANEL_PROFILE_PATH = os.path.join(os.path.dirname(__file__),'Door Profiles','Panel Profiles')
INSET_PROFILE_PATH = os.path.join(os.path.dirname(__file__),'Door Profiles','Inset Profiles')
BEAD_PROFILE_PATH = os.path.join(os.path.dirname(__file__),'Door Profiles','Bead Profiles')
MATERIAL_PATH = os.path.join(os.path.dirname(__file__),'Materials')
PANEL_MATERIAL_PATH = os.path.join(os.path.dirname(__file__),'Panel Materials')

def inch(inch):
    """ Converts inch to meter
    """
    return round(inch / 39.3700787,6)

def get_object_from_path(path):
    with bpy.data.libraries.load(path) as (data_from, data_to):
        data_to.objects = data_from.objects
    for obj in data_to.objects:
        return obj

def get_material_from_path(path):
    with bpy.data.libraries.load(path) as (data_from, data_to):
        data_to.materials = data_from.materials
    for mat in data_to.materials:
        return mat

def get_image_enum_previews(path,key,force_reload=False):
    """ Returns: ImagePreviewCollection
        Par1: path - The path to collect the images from
        Par2: key - The dictionary key the previews will be stored in
    """
    enum_items = []
    if len(key.my_previews) > 0:
        return key.my_previews
    
    if path and os.path.exists(path):
        blend_paths = []
        for fn in os.listdir(path):
            if fn.lower().endswith(".blend"):
                blend_paths.append(fn)

        for i, name in enumerate(blend_paths):
            filepath = os.path.join(path, name)
            thumb = key.load(filepath, "", 'IMAGE')
            filename, ext = os.path.splitext(name)
            enum_items.append((filename, filename, filename, thumb.icon_id, i))
    
    key.my_previews = enum_items
    key.my_previews_dir = path
    return key.my_previews

def create_image_preview_collection():
    import bpy.utils.previews
    col = bpy.utils.previews.new()
    col.my_previews_dir = ""
    col.my_previews = ()
    return col         

preview_collections = {}
preview_collections["outer_profiles"] = create_image_preview_collection()
preview_collections["inner_profiles"] = create_image_preview_collection()
preview_collections["panel_profiles"] = create_image_preview_collection()
preview_collections["inset_profiles"] = create_image_preview_collection()
preview_collections["bead_profiles"] = create_image_preview_collection()
preview_collections["materials"] = create_image_preview_collection()
preview_collections["panel_materials"] = create_image_preview_collection()

def enum_outer_profiles(self,context):
    if context is None:
        return []
    return get_image_enum_previews(OUTER_PROFILE_PATH,preview_collections["outer_profiles"])

def enum_inner_profiles(self,context):
    if context is None:
        return []
    return get_image_enum_previews(INNER_PROFILE_PATH,preview_collections["inner_profiles"])

def enum_panel_profiles(self,context):
    if context is None:
        return []
    return get_image_enum_previews(PANEL_PROFILE_PATH,preview_collections["panel_profiles"])

def enum_inset_profiles(self,context):
    if context is None:
        return []
    return get_image_enum_previews(INSET_PROFILE_PATH,preview_collections["inset_profiles"])

def enum_bead_profiles(self,context):
    if context is None:
        return []
    return get_image_enum_previews(BEAD_PROFILE_PATH,preview_collections["bead_profiles"])

def enum_materials(self,context):
    if context is None:
        return []
    return get_image_enum_previews(MATERIAL_PATH,preview_collections["materials"])

def enum_panel_materials(self,context):
    if context is None:
        return []
    return get_image_enum_previews(PANEL_MATERIAL_PATH,preview_collections["panel_materials"])

class Cabinet_Door_Scene_Props(PropertyGroup):

    door_tabs: EnumProperty(name="Door Tabs",
                            items=[('Current Door',"Current Door","Current Door"),
                                   ('New Door',"New Door","New Door")],
                            default='Current Door')# type: ignore
        
    door_x_dim: FloatProperty(name="Door X Dim",
                              description="The default x dim of the door",
                              default=inch(30),
                              unit='LENGTH')# type: ignore
        
    door_y_dim: FloatProperty(name="Door Y Dim",
                              description="The default y dim of the door",
                              default=inch(18),
                              unit='LENGTH')# type: ignore

    door_shape: EnumProperty(name="Door Shape",
                            items=[('Slab',"Slab","Slab"),
                                   ('Square',"Square","Square"),
                                   ('Crown',"Crown","Crown"),
                                   ('Arch',"Arch","Arch"),
                                   ('Dbl Crown',"Dbl Crown","Dbl Crown"),
                                   ('Dbl Arch',"Dbl Arch","Dbl Arch"),
                                   ('Twin',"Twin","Twin")],
                            default='Slab')# type: ignore
    
    insert_type: EnumProperty(name="Insert Type",
                            items=[('Solid Wood',"Solid Wood","Solid Wood"),
                                   ('Wood Mullion',"Wood Mullion","Wood Mullion"),
                                   ('Mission',"Mission","Mission"),
                                   ('Prairie',"Prairie","Prairie"),
                                   ('X',"X","X"),
                                   ('Double Bow',"Double Bow","Double Bow"),
                                   ('Gothic',"Gothic","Gothic"),
                                   ('Double Gothic',"Double Gothic","Double Gothic"),
                                   ('Interloken',"Interloken","Interloken")],
                            default='Solid Wood')# type: ignore

    panel_type: EnumProperty(name="Panel Type",
                             items=[('Raised Panel',"Raised Panel","Raised Panel"),
                                    ('Inset Panel',"Inset Panel","Inset Panel")],
                             default='Raised Panel')# type: ignore
        
    joinery_type: EnumProperty(name="Joinery Type",
                             items=[('Cope and Stick',"Cope and Stick","Cope and Stick"),
                                    ('Mitered',"Mitered","Mitered")],
                             default='Cope and Stick')# type: ignore

    material: EnumProperty(name="Material",
                           items=enum_materials)# type: ignore
    
    change_inset_panel_material: BoolProperty(name="Change Inset Panel Material",
                                        default=False)# type: ignore

    panel_material: EnumProperty(name="Panel Material",
                           items=enum_panel_materials)# type: ignore

    outer_profile: EnumProperty(name="Outer Profile",
                                items=enum_outer_profiles)# type: ignore
    
    include_inner_profile: BoolProperty(name="Include Inner Profile",
                                        default=False)# type: ignore

    inner_profile: EnumProperty(name="Inner Profile",
                                items=enum_inner_profiles)# type: ignore

    panel_profile: EnumProperty(name="Panel Profile",
                                items=enum_panel_profiles)# type: ignore        

    include_inset_profile: BoolProperty(name="Include Inset Profile",
                                        default=False)# type: ignore
    
    inset_profile: EnumProperty(name="Inset Profile",
                                items=enum_inset_profiles)# type: ignore  
    
    include_bead_profile: BoolProperty(name="Include Inset Profile",
                                        default=False)# type: ignore
        
    bead_profile: EnumProperty(name="Bead Profile",
                                items=enum_bead_profiles)# type: ignore  
        
    inset_amount: FloatProperty(name="Inset Amount",
                                description="The amount to inset the inner profile",
                                default=inch(2),
                                unit='LENGTH')# type: ignore

    left_stile_width: FloatProperty(name="Left Stile Width",
                                    description="The width of the left stile",
                                    default=inch(2),
                                    unit='LENGTH')# type: ignore
    
    right_stile_width: FloatProperty(name="Right Stile Width",
                                    description="The width of the right stile",
                                    default=inch(2),
                                    unit='LENGTH')# type: ignore

    top_rail_width: FloatProperty(name="Top Rail Width",
                                    description="The width of the top rail",
                                    default=inch(2),
                                    unit='LENGTH')# type: ignore
    
    bottom_rail_width: FloatProperty(name="Bottom Rail Width",
                                    description="The width of the top rail",
                                    default=inch(2),
                                    unit='LENGTH')# type: ignore
        
    def get_outer_profile_object(self):
        if self.outer_profile in bpy.data.objects:
            outer_profile = bpy.data.objects[self.outer_profile]
        else:
            path = os.path.join(OUTER_PROFILE_PATH,self.outer_profile + ".blend")
            outer_profile = get_object_from_path(path)
        return outer_profile

    def get_inner_profile_object(self):
        if self.inner_profile in bpy.data.objects:
            inner_profile = bpy.data.objects[self.inner_profile]
        else:
            path = os.path.join(INNER_PROFILE_PATH,self.inner_profile + ".blend")
            inner_profile = get_object_from_path(path)
        return inner_profile
    
    def get_panel_profile_object(self):
        if self.panel_profile in bpy.data.objects:
            panel_profile = bpy.data.objects[self.panel_profile]
        else:
            path = os.path.join(PANEL_PROFILE_PATH,self.panel_profile + ".blend")
            panel_profile = get_object_from_path(path)
        return panel_profile

    def get_inset_profile_object(self):
        if self.inset_profile in bpy.data.objects:
            inset_profile = bpy.data.objects[self.inset_profile]
        else:
            path = os.path.join(INSET_PROFILE_PATH,self.inset_profile + ".blend")
            inset_profile = get_object_from_path(path)
        return inset_profile
    
    def get_bead_profile_object(self):
        if self.bead_profile in bpy.data.objects:
            bead_profile = bpy.data.objects[self.bead_profile]
        else:
            path = os.path.join(BEAD_PROFILE_PATH,self.bead_profile + ".blend")
            bead_profile = get_object_from_path(path)
        return bead_profile
        
    def get_material(self):
        if self.material in bpy.data.materials:
            material = bpy.data.materials[self.material]
        else:
            path = os.path.join(MATERIAL_PATH,self.material + ".blend")
            material = get_material_from_path(path)
        return material        

    def get_panel_material(self):
        if self.panel_material in bpy.data.materials:
            panel_material = bpy.data.materials[self.panel_material]
        else:
            path = os.path.join(MATERIAL_PATH,self.panel_material + ".blend")
            panel_material = get_material_from_path(path)
        return panel_material   
    
    @classmethod
    def register(cls):
        bpy.types.Scene.cabinet_door_builder = PointerProperty(
            name="Cabinet Door Builder Props",
            description="Cabinet Door Builder Props",
            type=cls,
        )
        
    @classmethod
    def unregister(cls):
        del bpy.types.Scene.cabinet_door_builder    

classes = (
    Cabinet_Door_Scene_Props,
)

register, unregister = bpy.utils.register_classes_factory(classes)