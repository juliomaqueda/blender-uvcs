import bpy
from bpy.types import Operator

class PLASTIC_OT_open_unity_documentation(Operator):
    bl_idname = 'plastic.open_unity_documentation'
    bl_label = 'PlasticSCM website'
    bl_description = 'Open the PlasticSCM documentation in Unity\'s website'

    def execute(self, context):
        bpy.ops.wm.url_open(url='https://unity.com/products/plastic-scm')

        return {'FINISHED'}


def register():
    bpy.utils.register_class(PLASTIC_OT_open_unity_documentation)

def unregister():
    bpy.utils.unregister_class(PLASTIC_OT_open_unity_documentation)
