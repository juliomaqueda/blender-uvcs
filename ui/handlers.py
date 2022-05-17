import bpy
from bpy.app.handlers import persistent

from ..plastic import client

__current_file = None

@persistent
def plastic_on_load(_):
    global __current_file

    if bpy.data.filepath != '' and bpy.data.filepath != __current_file:
        client.clear_cache()

        __current_file = bpy.data.filepath

@persistent
def plastic_on_save(_):
    client.refresh_status()


def register():
    if not plastic_on_load in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.append(plastic_on_load)

    if not plastic_on_save in bpy.app.handlers.save_post:
        bpy.app.handlers.save_post.append(plastic_on_save)

def unregister():
    bpy.app.handlers.load_post.remove(plastic_on_load)
    bpy.app.handlers.save_post.remove(plastic_on_save)
