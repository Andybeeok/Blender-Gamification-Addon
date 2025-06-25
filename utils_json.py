import bpy
import json
import os

def obtener_ruta_json(nombre_archivo):
    """
    Retorna la ruta absoluta al archivo JSON dentro del addon.
    Los JSON deben estar en la carpeta 'data/'.
    """
    addon_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(addon_path, "data", nombre_archivo)

def cargar_json(nombre_archivo, default=None):
    ruta = obtener_ruta_json(nombre_archivo)
    if os.path.exists(ruta):
        try:
            with open(ruta, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"[ERROR] No se pudo leer {nombre_archivo}: {e}")
    return default if default is not None else {}

def guardar_json(nombre_archivo, datos):
    ruta = obtener_ruta_json(nombre_archivo)
    try:
        with open(ruta, 'w', encoding='utf-8') as f:
            json.dump(datos, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"[ERROR] No se pudo guardar {nombre_archivo}: {e}")

# Función opcional para registrar si se desea integrar algo a futuro
def register():
    pass

def unregister():
    pass
