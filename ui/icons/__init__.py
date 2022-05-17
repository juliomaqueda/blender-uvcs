import bpy.utils.previews
import os

__preview_collections = {}

__PLASTIC_ICONS = {
    'LOGO_PLASTIC': 'icon_plastic.png',
    'LOGO_PLASTIC_CHANGES': 'icon_plastic_notify.png',

    'LOGO_UNITY': 'icon_unity.png',

    'CREATE': 'icon_create.png',
    'REFRESH': 'icon_refresh.png'
}

def get_icon(name):
    plastic_icons = __preview_collections['plastic_icons']
    icon = plastic_icons.get(name)
    return icon.icon_id if icon else 0


def register():
    plastic_icons = bpy.utils.previews.new()
    __preview_collections['plastic_icons'] = plastic_icons

    for name, filename in __PLASTIC_ICONS.items():
        icon_path = os.path.join(os.path.dirname(__file__), filename)
        plastic_icons.load(name, icon_path, 'IMAGE')

def unregister():
    for plastic_icons in __preview_collections.values():
        bpy.utils.previews.remove(plastic_icons)

    __preview_collections.clear()
