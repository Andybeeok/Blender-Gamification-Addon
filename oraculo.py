# Código actualizado de oraculo.py

import bpy
import os
import subprocess
import random
from . import utils_json

# === Constantes y rutas ===
CARPETA_ADDON = os.path.dirname(__file__)
CARPETA_DATA = os.path.join(CARPETA_ADDON, "data")
CARPETA_ORACULO = os.path.join(CARPETA_ADDON, "oraculo")

ARCHIVOS_JSON_DISPONIBLES = [
    "configuracion.json",
    "tareas.json",
    "historial.json",
    "arbol_habilidades.json",
    "misiones_secundarias.json"
]

# ============= OPERADORES =============

class ORACULO_OT_MostrarInfo(bpy.types.Operator):
    bl_idname = "oraculo.mostrar_info"
    bl_label = "Información del Addon"
    bl_description = "Abre una nueva ventana con información editable sobre el addon"

    def execute(self, context):
        nombre_texto = "INFO_ORACULO"

        # Crea texto si no existe
        if nombre_texto not in bpy.data.texts:
            txt = bpy.data.texts.new(nombre_texto)
            txt.write("# 🧠 Acerca de Blender Gamification Addon\n")
            txt.write("Addon desarrollado por Andrés Castro 🎓\n")
            txt.write("Proyecto final del Máster en Artes Visuales y Multimedia (UPV) - Publicado el 1 de Julio de 2025\n\n")

            txt.write("## 🎯 Objetivo del Addon\n")
            txt.write("Gamification Addon busca promover el aprendizaje libre, autónomo y lúdico de Blender 3D.\n")
            txt.write("Cada herramienta, reto o modo de juego está diseñado para acompañarte en tu desarrollo creativo.\n\n")

            txt.write("## 📚 Contexto Pedagógico\n")
            txt.write("Este proyecto está fundamentado en principios de pedagogía activa, juego serio y autoevaluación.\n")
            txt.write("Incorpora elementos de gamificación como rangos, metas, misiones y progreso por dominios técnicos.\n\n")

            txt.write("## 🤖 ¿Cómo funciona?\n")
            txt.write("El Addon se organiza en paneles temáticos accesibles desde la barra lateral (N) de Blender:\n")
            txt.write("- **Define tu Rango:** Selecciona tu nivel manualmente.\n")
            txt.write("- **Hoja de Ruta:** Plantea objetivos en función de tu nivel y comienza tu recorrido.\n")
            txt.write("- **Mapa del Aventurero:** Recoge hábitos, tareas, metas y activa más de 250 sugerencias inteligentes.\n")
            txt.write("- **Escalera al Cielo:** Explora el árbol de habilidades y contenidos por dominios técnicos.\n")
            txt.write("- **Oráculo de la Sabiduría:** Inicia modos de juego, misiones y puzles para aprender jugando.\n\n")

            txt.write("## ⚙️ Aprendizaje Libre y Autónomo\n")
            txt.write("Todos los datos son modificables por el usuario. El sistema no impone caminos ni bloquea funciones.\n")
            txt.write("El progreso es personal y flexible. No hay penalizaciones. 💡 Aprende a tu ritmo.\n\n")

            txt.write("## 🛠️ ¿Cómo editar el contenido educativo?\n")
            txt.write("1. Ve a la carpeta raíz donde está instalado el Addon.\n")
            txt.write("2. Entra en la carpeta `/data/`\n")
            txt.write("3. Abre los archivos `.json` con un editor de texto externo (como Visual Studio Code).\n")
            txt.write("4. Edita hábitos, tareas, habilidades, niveles y más.\n")
            txt.write("⚠️ Por ahora no es posible modificar esta base desde dentro de Blender.\n\n")

            txt.write("## 🗂️ Estructura del Addon:\n")
            txt.write("gamification_addon/\n")
            txt.write("├── __init__.py                  ← Control central: importa y registra todo\n")
            txt.write("├── utils_json.py                ← Funciones comunes para cargar/guardar JSON\n")
            txt.write("├── rango.py                     ← Define tu Rango\n")
            txt.write("├── hoja_de_ruta.py              ← Objetivos personalizados (Fuzzy Matching)\n")
            txt.write("├── mapa_aventuras.py           ← Hábitos, Tareas y Metas\n")
            txt.write("├── escalera_cielo.py           ← Árbol de habilidades (referencia técnica)\n")
            txt.write("├── oraculo.py                   ← Modos de juego y misiones\n")
            txt.write("├── data/                        ← Archivos educativos en JSON\n")
            txt.write("│   ├── configuracion.json\n")
            txt.write("│   ├── tareas.json\n")
            txt.write("│   ├── historial.json\n")
            txt.write("│   ├── arbol_habilidades.json\n")
            txt.write("│   └── misiones_secundarias.json\n")
            txt.write("├── dominios/                   ← Aloja los Archivos .blend del árbol de habilidades\n")
            txt.write("├── oraculo/                    ← Aloja los Archivos .blend de modos de juego\n")
            txt.write("└── icons/                      ← Aloja los Íconos personalizados (opcional)\n\n")

            txt.write("¡Gracias por usar este addon eduativo! 🚀\n")
            txt.write("Más información: @Andy.Beeok (ArtStation / Behance / Intagram / LinkedIn / Twiter)\n")
            txt.write("20andrescastro20@gmail.com\n")

        else:
            txt = bpy.data.texts[nombre_texto]

        # Abre nueva ventana
        bpy.ops.wm.window_new()
        new_window = context.window_manager.windows[-1]

        # Buscar el area TEXT_EDITOR en la nueva ventana
        for area in new_window.screen.areas:
            area.type = 'TEXT_EDITOR'
            for space in area.spaces:
                if space.type == 'TEXT_EDITOR':
                    space.text = txt
                    break

        return {'FINISHED'}

# ============= MODO CREATIVO =============

class ORACULO_OT_AbrirBlend(bpy.types.Operator):
    bl_idname = "oraculo.abrir_blend"
    bl_label = "Abrir Proyecto Blender"
    bl_description = "Abre un archivo .blend externo relacionado con el modo de juego seleccionado"

    filepath: bpy.props.StringProperty()

    def execute(self, context):
        ruta = os.path.join(CARPETA_ORACULO, self.filepath)
        if not os.path.exists(ruta):
            self.report({'ERROR'}, f"Archivo no encontrado: {ruta}")
            return {'CANCELLED'}

        blender_exe = bpy.app.binary_path
        subprocess.Popen([blender_exe, ruta])
        return {'FINISHED'}

# ============= MISIONES SECUNDARIAS =============

class ORACULO_OT_LanzarDado(bpy.types.Operator):
    bl_idname = "oraculo.lanzar_dado"
    bl_label = "Lanzar Dado de Misión"
    bl_description = "Genera una misión aleatoria con tema, nicho y restricción para incentivar la creatividad"

    def execute(self, context):
        ruta_json = os.path.join(CARPETA_DATA, "misiones_secundarias.json")
        datos = utils_json.cargar_json(ruta_json)

        tema = random.choice(datos.get("temas", []))
        nicho = random.choice(datos.get("nichos", []))
        restriccion = random.choice(datos.get("restricciones", []))
        scene = context.scene
        scene.oraculo_resultados_mision.clear()

        for frase in [f"1. {tema}", f"2. {nicho}", f"3. {restriccion}"]:
            item = scene.oraculo_resultados_mision.add()
            item.name = frase
        return {'FINISHED'}

# ============= PROBLEMAS Y PUZLES =============
# === ILUMINACIÓN ===
class ORACULO_OT_Puzzle_Iluminacion(bpy.types.Operator):
    bl_idname = "oraculo.puzzle_iluminacion"
    bl_label = "Iluminación"
    bl_description = "Resolver retos sobre iluminación, luces y atmósferas."

    def execute(self, context):
        ruta = os.path.join(CARPETA_ORACULO, "puzzle_iluminacion_1.blend")
        if not os.path.exists(ruta):
            self.report({'ERROR'}, f"Archivo no encontrado: {ruta}")
            return {'CANCELLED'}
        subprocess.Popen([bpy.app.binary_path, ruta])
        return {'FINISHED'}

# === MODELADO ===
class ORACULO_OT_Puzzle_Modelado(bpy.types.Operator):
    bl_idname = "oraculo.puzzle_modelado"
    bl_label = "Modelado"
    bl_description = "Resolver puzzles sobre formas, topología y técnicas de modelado 3D."

    def execute(self, context):
        ruta = os.path.join(CARPETA_ORACULO, "puzzle_modelado_retopologia_1.blend")
        if not os.path.exists(ruta):
            self.report({'ERROR'}, f"Archivo no encontrado: {ruta}")
            return {'CANCELLED'}
        subprocess.Popen([bpy.app.binary_path, ruta])
        return {'FINISHED'}

# === TEXTURIZADO ===
class ORACULO_OT_Puzzle_Texturizado(bpy.types.Operator):
    bl_idname = "oraculo.puzzle_texturizado"
    bl_label = "Texturizado"
    bl_description = "Explora mapas UV, materiales y técnicas de shading en contextos prácticos."

    def execute(self, context):
        ruta = os.path.join(CARPETA_ORACULO, "puzzle_texturizado_1.blend")
        if not os.path.exists(ruta):
            self.report({'ERROR'}, f"Archivo no encontrado: {ruta}")
            return {'CANCELLED'}
        subprocess.Popen([bpy.app.binary_path, ruta])
        return {'FINISHED'}
    
# === ANIMACIÓN ===
class ORACULO_OT_Puzzle_Animacion(bpy.types.Operator):
    bl_idname = "oraculo.puzzle_animacion"
    bl_label = "Animación"
    bl_description = "Domina curvas de animación, keyframes y rigs con misiones guiadas."

    def execute(self, context):
        ruta = os.path.join(CARPETA_ORACULO, "puzzle_animacion_1.blend")
        if not os.path.exists(ruta):
            self.report({'ERROR'}, f"Archivo no encontrado: {ruta}")
            return {'CANCELLED'}
        subprocess.Popen([bpy.app.binary_path, ruta])
        return {'FINISHED'}
    
# === SIMULACIÓN ===
class ORACULO_OT_Puzzle_Simulacion(bpy.types.Operator):
    bl_idname = "oraculo.puzzle_simulacion"
    bl_label = "Simulación"
    bl_description = "Experimenta con físicas, fluidos, colisiones y simulaciones dinámicas."

    def execute(self, context):
        ruta = os.path.join(CARPETA_ORACULO, "puzzle_simulacion_1.blend")
        if not os.path.exists(ruta):
            self.report({'ERROR'}, f"Archivo no encontrado: {ruta}")
            return {'CANCELLED'}
        subprocess.Popen([bpy.app.binary_path, ruta])
        return {'FINISHED'}

# === DISEÑO PROCEDURAL ===
class ORACULO_OT_Puzzle_Procedural(bpy.types.Operator):
    bl_idname = "oraculo.puzzle_procedural"
    bl_label = "Diseño Procedural"
    bl_description = "Aprende geometría nodal, instanciación y generadores automáticos."

    def execute(self, context):
        ruta = os.path.join(CARPETA_ORACULO, "puzzle_procedural_1.blend")
        if not os.path.exists(ruta):
            self.report({'ERROR'}, f"Archivo no encontrado: {ruta}")
            return {'CANCELLED'}
        subprocess.Popen([bpy.app.binary_path, ruta])
        return {'FINISHED'}

# === POSTPROCDUCCIÓN ===
class ORACULO_OT_Puzzle_Postproduccion(bpy.types.Operator):
    bl_idname = "oraculo.puzzle_postproduccion"
    bl_label = "Postproducción"
    bl_description = "Edita con el Video Editor y el Compositor para dar el acabado final a tus renders."

    def execute(self, context):
        ruta = os.path.join(CARPETA_ORACULO, "puzzle_postproduccion_retopologia_1.blend")
        if not os.path.exists(ruta):
            self.report({'ERROR'}, f"Archivo no encontrado: {ruta}")
            return {'CANCELLED'}
        subprocess.Popen([bpy.app.binary_path, ruta])
        return {'FINISHED'}

# === EFECTOS ESPECIALES ===
class ORACULO_OT_Puzzle_VFX(bpy.types.Operator):
    bl_idname = "oraculo.puzzle_vfx"
    bl_label = "Efectos Especiales"
    bl_description = "Simula efectos especiales, partículas, humo y energía visual avanzada."

    def execute(self, context):
        ruta = os.path.join(CARPETA_ORACULO, "puzzle_vfx_1.blend")
        if not os.path.exists(ruta):
            self.report({'ERROR'}, f"Archivo no encontrado: {ruta}")
            return {'CANCELLED'}
        subprocess.Popen([bpy.app.binary_path, ruta])
        return {'FINISHED'}
    
# === CÓDIGO ===
class ORACULO_OT_Puzzle_Codigo(bpy.types.Operator):
    bl_idname = "oraculo.puzzle_codigo"
    bl_label = "Código"
    bl_description = "Automatiza tareas y crea herramientas propias usando scripting en Blender."

    def execute(self, context):
        ruta = os.path.join(CARPETA_ORACULO, "puzzle_codigo_1.blend")
        if not os.path.exists(ruta):
            self.report({'ERROR'}, f"Archivo no encontrado: {ruta}")
            return {'CANCELLED'}
        subprocess.Popen([bpy.app.binary_path, ruta])
        return {'FINISHED'}
    
# === PIPELINE Y PRODUCCÍÓN ===
class ORACULO_OT_Puzzle_Pipeline(bpy.types.Operator):
    bl_idname = "oraculo.puzzle_pipeline"
    bl_label = "Pipeline y Producción"
    bl_description = "Explora flujos de trabajo, optimización y colaboración en producción Blender."

    def execute(self, context):
        ruta = os.path.join(CARPETA_ORACULO, "puzzle_pipeline_1.blend")
        if not os.path.exists(ruta):
            self.report({'ERROR'}, f"Archivo no encontrado: {ruta}")
            return {'CANCELLED'}
        subprocess.Popen([bpy.app.binary_path, ruta])
        return {'FINISHED'}

# ============= PANEL PRINCIPAL =============

class PANEL_PT_Oraculo(bpy.types.Panel):
    bl_label = "El Oráculo de la Sabiduría"
    bl_idname = "PANEL_PT_oraculo"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Gamification'

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # Información
        layout.label(text="Información del Addon:")
        layout.operator("oraculo.mostrar_info", text="Acerca del Addon", icon='INFO')

        layout.separator()

        # === Subtema colapsable ===
        layout.prop(scene, "mostrar_modos_juego", toggle=True, text="Modos de Juego")
        if scene.mostrar_modos_juego:

            # Modo Creativo
            box = layout.box()
            box.label(text="Modo Creativo:")
            box.operator("oraculo.abrir_blend", text="Comenzar", icon='PLAY').filepath = "modo_creativo_1.blend"

            # Misiones Secundarias
            box = layout.box()
            box.label(text="Misiones Secundarias:")
            box.operator("oraculo.lanzar_dado", text="Lanzar el Dado", icon='CUBE')
            box.label(text="Resultado:")
            for item in scene.oraculo_resultados_mision:
                box.box().label(text=item.name)

            # Problemas y Puzzles
            box = layout.box()
            box.label(text="Problemas y Puzzles:")

            # En filas de 2 botones por fila
            fila = box.row()
            fila.operator("oraculo.puzzle_iluminacion", text="Iluminación", icon="LIGHT")
            fila.operator("oraculo.puzzle_modelado", text="Modelado", icon="MESH_CUBE")

            fila = box.row()
            fila.operator("oraculo.puzzle_texturizado", text="Texturizado", icon="TEXTURE")
            fila.operator("oraculo.puzzle_animacion", text="Animación", icon="ARMATURE_DATA")

            fila = box.row()
            fila.operator("oraculo.puzzle_simulacion", text="Simulación", icon="MOD_PHYSICS")
            fila.operator("oraculo.puzzle_procedural", text="Procedural", icon="GEOMETRY_NODES")

            fila = box.row()
            fila.operator("oraculo.puzzle_postproduccion", text="Postproducción", icon="SEQUENCE")
            fila.operator("oraculo.puzzle_vfx", text="VFX", icon="FORCE_FORCE")

            fila = box.row()
            fila.operator("oraculo.puzzle_codigo", text="Código", icon="CONSOLE")
            fila.operator("oraculo.puzzle_pipeline", text="Pipeline", icon="PRESET")

# === REGISTRO ===

def register():
    bpy.utils.register_class(ORACULO_OT_MostrarInfo)
    bpy.utils.register_class(ORACULO_OT_AbrirBlend)
    bpy.utils.register_class(ORACULO_OT_LanzarDado)
    bpy.utils.register_class(PANEL_PT_Oraculo)
    bpy.utils.register_class(ORACULO_OT_Puzzle_Iluminacion)
    bpy.utils.register_class(ORACULO_OT_Puzzle_Modelado)
    bpy.utils.register_class(ORACULO_OT_Puzzle_Texturizado)
    bpy.utils.register_class(ORACULO_OT_Puzzle_Animacion)
    bpy.utils.register_class(ORACULO_OT_Puzzle_Simulacion)
    bpy.utils.register_class(ORACULO_OT_Puzzle_Procedural)
    bpy.utils.register_class(ORACULO_OT_Puzzle_Postproduccion)
    bpy.utils.register_class(ORACULO_OT_Puzzle_VFX)
    bpy.utils.register_class(ORACULO_OT_Puzzle_Codigo)
    bpy.utils.register_class(ORACULO_OT_Puzzle_Pipeline)

    bpy.types.Scene.oraculo_resultados_mision = bpy.props.CollectionProperty(type=bpy.types.PropertyGroup)
    bpy.types.Scene.mostrar_modos_juego = bpy.props.BoolProperty(
        name="Mostrar Modos de Juego",
        description="Activa o desactiva la visualización de Modo Creativo, Misiones y Puzles",
        default=False
    )

def unregister():
    bpy.utils.unregister_class(ORACULO_OT_MostrarInfo)
    bpy.utils.unregister_class(ORACULO_OT_AbrirBlend)
    bpy.utils.unregister_class(ORACULO_OT_LanzarDado)
    bpy.utils.unregister_class(PANEL_PT_Oraculo)
    bpy.utils.unregister_class(ORACULO_OT_Puzzle_Iluminacion)
    bpy.utils.unregister_class(ORACULO_OT_Puzzle_Modelado)
    bpy.utils.unregister_class(ORACULO_OT_Puzzle_Texturizado)
    bpy.utils.unregister_class(ORACULO_OT_Puzzle_Animacion)
    bpy.utils.unregister_class(ORACULO_OT_Puzzle_Simulacion)
    bpy.utils.unregister_class(ORACULO_OT_Puzzle_Procedural)
    bpy.utils.unregister_class(ORACULO_OT_Puzzle_Postproduccion)
    bpy.utils.unregister_class(ORACULO_OT_Puzzle_VFX)
    bpy.utils.unregister_class(ORACULO_OT_Puzzle_Codigo)
    bpy.utils.unregister_class(ORACULO_OT_Puzzle_Pipeline)

    del bpy.types.Scene.mostrar_modos_juego
    del bpy.types.Scene.oraculo_resultados_mision
