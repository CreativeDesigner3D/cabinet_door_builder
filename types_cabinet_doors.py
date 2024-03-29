import bpy
import os

GEO_NODE_DOOR_PATH = os.path.join(os.path.dirname(__file__),'GeoNodes')

class GeoNodeDoor():

    obj = None
    mod = None
    coll = None

    def __init__(self,obj=None,coll=None):
        if obj:
            self.obj = obj
            for mod in self.obj.modifiers:
                if mod.type == 'NODES':
                    self.mod = mod
                    break            
        if coll:
            self.coll = coll
        else:
            self.coll = bpy.context.view_layer.active_layer_collection.collection

    def get_geo_node(self,path,geo_node_name):
        ''' Get the Geo Node
            If the Node Group is already in data use that
            otherwise get object from file
        '''
        if geo_node_name in bpy.data.node_groups:
            node = bpy.data.node_groups[geo_node_name]
            cage = bpy.data.meshes.new(geo_node_name)
            self.obj = bpy.data.objects.new(geo_node_name,cage)
            self.mod = self.obj.modifiers.new('GeometryNodes','NODES')
            self.mod.node_group = node
        else:
            with bpy.data.libraries.load(path) as (data_from, data_to):
                data_to.objects = data_from.objects
            for obj in data_to.objects:
                self.obj = obj
            self.obj.name = geo_node_name
            for mod in self.obj.modifiers:
                if mod.type == 'NODES':
                    self.mod = mod
                    break        

    def set_input(self,name,value=None):
        if name in self.mod.node_group.interface.items_tree:
            node_input = self.mod.node_group.interface.items_tree[name]             
            exec('self.mod["' + node_input.identifier + '"] = value')    

    def create(self,name=""):
        door_name = self.__class__.__name__
        self.get_geo_node(os.path.join(GEO_NODE_DOOR_PATH,door_name +'.blend'),door_name)
        self.obj.name = name
        self.obj['GeoNodeName'] = door_name
        self.coll.objects.link(self.obj)    


class GeoNodeNewDoor(GeoNodeDoor):

    def create(self,name=""):
        door_name = self.__class__.__name__
        self.get_geo_node(os.path.join(GEO_NODE_DOOR_PATH,door_name +'.blend'),door_name)
        self.obj.name = name
        self.obj['GeoNodeName'] = door_name
        self.coll.objects.link(self.obj)    