import bpy
from bpy.props import BoolProperty, IntProperty, StringProperty
import os
import platform

from .. import common
from ..uvcs import client

DEFAULT_CM_PATH_LINUX_MAC = '/usr/local/bin/cm'
DEFAULT_CM_PATH_WINDOWS_32_BIT = 'C:\Program Files (x86)\PlasticSCM5\client\cm.exe'
DEFAULT_CM_PATH_WINDOWS_64_BIT = 'C:\Program Files\PlasticSCM5\client\cm.exe'

class UVCSPreferences(bpy.types.AddonPreferences):
    bl_idname = common.ADDON_NAME

    def __get_default_cm_path_by_os():
        # Windows
        if platform.architecture()[1] == 'WindowsPE':
            if platform.architecture()[0] == '64bit':
                default_cm_path = DEFAULT_CM_PATH_WINDOWS_64_BIT
            elif platform.architecture()[0] == '32bit':
                default_cm_path = DEFAULT_CM_PATH_WINDOWS_32_BIT
        # Linux and Mac
        else:
            default_cm_path = DEFAULT_CM_PATH_LINUX_MAC

        return default_cm_path

    def __update_cm_path(self, context):
        self.existing_cm_path = os.path.isfile(self.uvcs_cm_path)

        client.set_cm_location(self.uvcs_cm_path)
        client.refresh_status()

    uvcs_cm_path: StringProperty(
        name='Path to the Unity Version Control cm executable',
        subtype='FILE_PATH',
        update=__update_cm_path,
        default=__get_default_cm_path_by_os()
    )

    existing_cm_path: BoolProperty(default=True)

    popup_width: IntProperty(
        name='Popup width',
        description='Width to use for the Unity Version Control popup menu',
        min=300,
        max=400,
        default=300
    )

    def draw(self, context):
        layout = self.layout

        row = layout.row()

        col = row.column()
        col.scale_x=1.2
        col.prop(self, 'uvcs_cm_path', text='Path to cm', translate=False)

        col = row.column()
        col.prop(self, 'popup_width', slider=True, translate=False)

        if not self.existing_cm_path:
            row = layout.row()
            row.label(text='File path "' + self.uvcs_cm_path + '" doesn\'t exist', icon='ERROR', translate=False)

def register():
    bpy.utils.register_class(UVCSPreferences)

def unregister():
    bpy.utils.unregister_class(UVCSPreferences)
