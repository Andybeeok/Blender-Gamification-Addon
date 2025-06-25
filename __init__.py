bl_info = {
    "name": "Blender Gamification Addon",
    "blender": (4, 3, 0),
    "version": (1, 0, 0),
    "author": "Andrés Castro",
    "description": "Addon educativo con enfoque lúdico para el aprendizaje progresivo de Blender",
    "category": "Education"
}

import bpy
import importlib

# === Importación de módulos internos ===
from . import utils_json
from . import rango
from . import hoja_de_ruta
from . import mapa_aventuras
from . import escalera_cielo
from . import oraculo

# === Recarga de módulos en desarrollo ===
importlib.reload(utils_json)
importlib.reload(rango)
importlib.reload(hoja_de_ruta)
importlib.reload(mapa_aventuras)
importlib.reload(escalera_cielo)
importlib.reload(oraculo)

# === Registro ===
def register():
    utils_json.register()
    rango.register()
    hoja_de_ruta.register()
    mapa_aventuras.register()
    escalera_cielo.register()
    oraculo.register()

def unregister():
    oraculo.unregister()
    escalera_cielo.unregister()
    mapa_aventuras.unregister()
    hoja_de_ruta.unregister()
    rango.unregister()
    utils_json.unregister()

if __name__ == "__main__":
    register()
