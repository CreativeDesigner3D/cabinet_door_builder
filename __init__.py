from . import props_cabinet_doors
from . import ui_cabinet_doors
from . import ops_cabinet_doors

bl_info = {
    "name": "Cabinet Door Builder",
    "author": "Andrew Peel",
    "version": (4, 0, 2),
    "blender": (4, 0, 1),
    "location": "3D Viewport Sidebar",
    "description": "Library to Create Cabinet Doors",
    "warning": "",
    "wiki_url": "",
    "category": "Asset Library",
}


def register():
    props_cabinet_doors.register()
    ui_cabinet_doors.register()
    ops_cabinet_doors.register()


def unregister():
    props_cabinet_doors.unregister()
    ui_cabinet_doors.unregister()
    ops_cabinet_doors.unregister()