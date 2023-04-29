import bpy
from bpy.types import Operator

class UVCS_OT_open_unity_documentation(Operator):
    bl_idname = 'uvcs.open_unity_documentation'
    bl_label = 'Unity Version Control website'
    bl_description = 'Open the Unity Version Control documentation in Unity\'s website'

    def execute(self, context):
        bpy.ops.wm.url_open(url='https://unity.com/solutions/version-control')

        return {'FINISHED'}


def register():
    bpy.utils.register_class(UVCS_OT_open_unity_documentation)

def unregister():
    bpy.utils.unregister_class(UVCS_OT_open_unity_documentation)
