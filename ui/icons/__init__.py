import bpy.utils.previews
import os

__preview_collections = {}

__UVCS_ICONS = {
    'LOGO_UVCS': 'icon_devops.png',
    'LOGO_UVCS_CHANGES': 'icon_devops_notify.png',

    'LOGO_UNITY': 'icon_unity.png',

    'CREATE': 'icon_create.png',
    'REFRESH': 'icon_refresh.png'
}

def get_icon(name):
    uvcs_icons = __preview_collections['uvcs_icons']
    icon = uvcs_icons.get(name)
    return icon.icon_id if icon else 0


def register():
    uvcs_icons = bpy.utils.previews.new()
    __preview_collections['uvcs_icons'] = uvcs_icons

    for name, filename in __UVCS_ICONS.items():
        icon_path = os.path.join(os.path.dirname(__file__), filename)
        uvcs_icons.load(name, icon_path, 'IMAGE')

def unregister():
    for uvcs_icons in __preview_collections.values():
        bpy.utils.previews.remove(uvcs_icons)

    __preview_collections.clear()
