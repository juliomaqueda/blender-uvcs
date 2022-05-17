bl_info = {
    'name': 'PlasticSCM',
    'description': 'Integration with PlasticSCM version control system',
    'author': 'Julio Maqueda (@juliomaqueda)',
    'version': (0, 1, 0),
    'blender': (2, 80, 0),
    'location': 'Topbar / Sidebar -> PlasticSCM',
    'warning': '',
    'doc_url': 'https://github.com/juliomaqueda/blender-plasticscm/blob/main/README.md',
    'tracker_url': 'https://github.com/juliomaqueda/blender-plasticscm/issues',
    "support": "COMMUNITY",
    'category': 'Version control'
}

from . import ui
from .plastic import client

def register():
    ui.register()
    client.clear_cache()

def unregister():
    ui.unregister()

if __name__ == '__main__':
    register()
