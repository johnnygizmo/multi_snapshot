import bpy
import os
import random

def main(context):
    camera = bpy.data.objects["Camera"]
    areatype = context.area.type
    context.area.type = 'VIEW_3D'   
    oblist = context.selected_objects.copy()    
    bpy.ops.object.select_all(action='DESELECT')
    for ob in oblist:
        if ob.type == "CURVE":
            ob.asset_mark()
    for ob in oblist:
        if ob.type == "CURVE":
            ob.select_set(True)    
            context.view_layer.objects.active = ob
            bpy.ops.view3d.camera_to_view_selected()      
            camera.location[2] = camera.location[2] + 0.01    
            bpy.context.object.data.dimensions = '2D'
            bpy.context.object.data.fill_mode = 'BOTH'
            
            filename = str(random.randint(0,100000000000))+".png"
            filepath = str(os.path.abspath(os.path.join(os.sep, 'tmp', filename)))
            
            bpy.context.scene.render.filepath = filepath
            bpy.ops.render.render(write_still = True)
            override = bpy.context.copy()
            context.area.type = 'FILE_BROWSER'
            override['id'] = ob

            bpy.ops.ed.lib_id_load_custom_preview(override,filepath=filepath)
            context.area.type = 'VIEW_3D'   
            
            bpy.context.object.data.dimensions = '3D'
            bpy.context.object.data.fill_mode = 'HALF'           
            ob.select_set(False)   
            
            os.unlink(filepath)
            bpy.ops.object.select_all(action='DESELECT')
    context.area.type = areatype
                
class SimpleOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.simple_operator"
    bl_label = "Simple Object Operator"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        main(context)
        return {'FINISHED'}


def register():
    bpy.utils.register_class(SimpleOperator)


def unregister():
    bpy.utils.unregister_class(SimpleOperator)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.object.simple_operator()
