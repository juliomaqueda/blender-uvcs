bl_info = {
    'name': 'Unity Version Control',
    'description': 'Integration with Unity version control system',
    'author': 'Julio Maqueda (@juliomaqueda)',
    'version': (0, 1, 6),
    'blender': (2, 80, 0),
    'location': 'Topbar / Sidebar -> Unity version contol',
    'warning': '',
    'doc_url': 'https://github.com/juliomaqueda/blender-uvcs/blob/main/README.md',
    'tracker_url': 'https://github.com/juliomaqueda/blender-uvcs/issues',
    "support": "COMMUNITY",
    'category': 'Version control'
}

from . import ui
from .uvcs import client

def register():
    ui.register()
    client.clear_cache()

def unregister():
    ui.unregister()

if __name__ == '__main__':
    register()
