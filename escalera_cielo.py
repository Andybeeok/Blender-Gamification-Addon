import bpy
import os
import subprocess
from . import utils_json

ARCHIVO_JSON = "arbol_habilidades.json"


class EscaleraItem(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="Nombre")
    completed: bpy.props.BoolProperty(name="Completado", default=False)

#-------------------------------------------------------------------------------------------------------------

class ESCALERA_OT_AbrirBlendExterno(bpy.types.Operator):
    bl_idname = "escalera.abrir_blend_externo"
    bl_label = "Explorar Contenido Educativo (Externo)"
    bl_description = "Abre un archivo .blend con contenido didáctico del dominio."

    filepath: bpy.props.StringProperty(name="Ruta del Archivo .blend")

    def execute(self, context):
        addon_dir = os.path.dirname(__file__)
        ruta_blend = os.path.join(addon_dir, "dominios", self.filepath)

        if not os.path.exists(ruta_blend):
            self.report({'ERROR'}, f"Archivo no encontrado: {ruta_blend}")
            return {'CANCELLED'}

        blender_exe = bpy.app.binary_path
        try:
            subprocess.Popen([blender_exe, ruta_blend])
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"No se pudo abrir Blender:\n{e}")
            return {'CANCELLED'}

#-------------------------------------------------------------------------------------------------------------

# ============= FUNDAMENTOS DE CREACIÓN 3D =============
# === MODELADO ===
class ESCALERA_OT_CargarRetosModelado(bpy.types.Operator):
    bl_idname = "escalera.cargar_retos_modelado"
    bl_label = "Actualizar Retos de Modelado"
    bl_description = "Carga retos del dominio Modelado desde el archivo JSON."

    def execute(self, context):
        datos = utils_json.cargar_json(ARCHIVO_JSON)
        retos = datos.get("Fundamentos de Creación 3D", {}).get("Modelado", {}).get("retos", [])

        scene = context.scene
        scene.retos_modelado.clear()

        for reto in retos:
            item = scene.retos_modelado.add()
            item.name = reto
            item.completed = False

        return {'FINISHED'}

def draw_subtema_modelado(layout, scene, key):
    box = layout.box()
    box.label(text=f"{key.capitalize()}")
    box.prop(scene, f"mostrar_manual_{key}", toggle=True, text="Manual de Conocimientos", emboss=True)

    if getattr(scene, f"mostrar_manual_{key}", False):
        op = box.operator("escalera.abrir_blend_externo", text="Explorar Contenido Educativo", icon='FILE_FOLDER')
        op.filepath = "modelado.blend"  # Cambia según el dominio
        box.prop(scene, f"mostrar_retos_{key}", toggle=True, text="Retos", emboss=True)

        if getattr(scene, f"mostrar_retos_{key}", False):
            col = box.column()
            row = col.row()
            row.operator("escalera.cargar_retos_modelado", text="", icon="FILE_REFRESH")
            row.label(text="Actualizar Retos")

            col.label(text="Lista de Retos:")
            for reto in getattr(scene, f"retos_{key}", []):
                fila = col.row()
                fila.prop(reto, "completed", text=reto.name)

            total = len(getattr(scene, f"retos_{key}", []))
            completados = sum(1 for r in getattr(scene, f"retos_{key}", []) if r.completed)
            progreso = int((completados / total) * 100) if total > 0 else 0
            col.label(text=f"Progreso: {progreso}%")

#-------------------------------------------------------------------------------------------------------------

# ============= DINÁMICA Y EXPRESIÓN =============
# === ANIMACIÓN ===
class ESCALERA_OT_CargarRetosAnimacion(bpy.types.Operator):
    bl_idname = "escalera.cargar_retos"
    bl_label = "Actualizar Retos desde JSON"
    bl_description = "Abre la lista de Retos."
    
    def execute(self, context):
        datos = utils_json.cargar_json(ARCHIVO_JSON)
        retos = datos.get("Dinámica y Expresión", {}).get("Animación", {}).get("retos", [])

        scene = context.scene
        scene.retos_animacion.clear()

        for reto in retos:
            item = scene.retos_animacion.add()
            item.name = reto
            item.completed = False

        return {'FINISHED'}
    
def draw_subtema(layout, scene, key):
    box = layout.box()
    box.label(text=f"{key.capitalize()}")
    box.prop(scene, f"mostrar_manual_{key}", toggle=True, text="Manual de Conocimientos", emboss=True)

    if getattr(scene, f"mostrar_manual_{key}", False):
        op = box.operator("escalera.abrir_blend_externo", text="Explorar Contenido Educativo", icon='FILE_FOLDER')
        op.filepath = "animacion.blend"  # Cambia según el dominio
        box.prop(scene, f"mostrar_retos_{key}", toggle=True, text="Retos", emboss=True)

        if getattr(scene, f"mostrar_retos_{key}", False):
            col = box.column()
            row = col.row()
            row.operator("escalera.cargar_retos", text="", icon="FILE_REFRESH")
            row.label(text="Actualizar Retos")

            col.label(text="Lista de Retos:")
            for reto in getattr(scene, f"retos_{key}", []):
                fila = col.row()
                fila.prop(reto, "completed", text=reto.name)

            total = len(getattr(scene, f"retos_{key}", []))
            completados = sum(1 for r in getattr(scene, f"retos_{key}", []) if r.completed)
            progreso = int((completados / total) * 100) if total > 0 else 0
            col.label(text=f"Progreso: {progreso}%")

# ============= PRODUCCIÓN Y REFINAMIENTO =============
# === POSTPRODUCCIÓN ===
class ESCALERA_OT_CargarRetosPostProduccion(bpy.types.Operator):
    bl_idname = "escalera.cargar_retos_postproduccion"
    bl_label = "Actualizar Retos de Postproducción"
    bl_description = "Carga los retos específicos para el dominio de postproducción."

    def execute(self, context):
        datos = utils_json.cargar_json(ARCHIVO_JSON)
        retos = datos.get("Producción y Refinamiento", {}).get("Postproducción", {}).get("retos", [])

        scene = context.scene
        scene.retos_postproduccion.clear()

        for reto in retos:
            item = scene.retos_postproduccion.add()
            item.name = reto
            item.completed = False

        return {'FINISHED'}

def draw_subtema_postproduccion(layout, scene, key):
    box = layout.box()
    box.label(text=f"{key.capitalize()}")
    box.prop(scene, f"mostrar_manual_{key}", toggle=True, text="Manual de Conocimientos", emboss=True)

    if getattr(scene, f"mostrar_manual_{key}", False):
        op = box.operator("escalera.abrir_blend_externo", text="Explorar Contenido Educativo", icon='FILE_FOLDER')
        op.filepath = "postproduccion.blend" # Cambia según el dominio
        box.prop(scene, f"mostrar_retos_{key}", toggle=True, text="Retos", emboss=True)

        if getattr(scene, f"mostrar_retos_{key}", False):
            col = box.column()
            row = col.row()
            row.operator("escalera.cargar_retos_postproduccion", text="", icon="FILE_REFRESH")
            row.label(text="Actualizar Retos")

            col.label(text="Lista de Retos:")
            for reto in getattr(scene, f"retos_{key}", []):
                fila = col.row()
                fila.prop(reto, "completed", text=reto.name)

            total = len(getattr(scene, f"retos_{key}", []))
            completados = sum(1 for r in getattr(scene, f"retos_{key}", []) if r.completed)
            progreso = int((completados / total) * 100) if total > 0 else 0
            col.label(text=f"Progreso: {progreso}%")

#-------------------------------------------------------------------------------------------------------------

class PANEL_PT_EscaleraCielo(bpy.types.Panel):
    bl_label = "La Escalera al Cielo"
    bl_idname = "PANEL_PT_escalera_cielo"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Gamification'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        layout.label(text="Árbol de Habilidades:")
        # === FUNDAMENTOS DE CREACIÓN 3D ===
        layout.prop(scene, "mostrar_modelado", toggle=True, text="Fundamentos de Creación 3D")
        if scene.mostrar_modelado:
            draw_subtema_modelado(layout, scene, "modelado")
        # === DINÁMICA Y EXPRESIÓN ===
        layout.prop(scene, "mostrar_animacion", toggle=True, text="Dinámica y Expresión")
        if scene.mostrar_animacion:
            draw_subtema(layout, scene, "animacion")
        # === PRODUCCIÓN Y REFINAMIENTO ===
        layout.prop(scene, "mostrar_produccion", toggle=True, text="Producción y Refinamiento")
        if scene.mostrar_produccion:
            draw_subtema_postproduccion(layout, scene, "postproduccion")

#-------------------------------------------------------------------------------------------------------------

def register():
    bpy.utils.register_class(EscaleraItem)
    bpy.utils.register_class(ESCALERA_OT_AbrirBlendExterno)
    bpy.utils.register_class(ESCALERA_OT_CargarRetosModelado)
    bpy.utils.register_class(ESCALERA_OT_CargarRetosAnimacion)
    bpy.utils.register_class(ESCALERA_OT_CargarRetosPostProduccion)
    bpy.utils.register_class(PANEL_PT_EscaleraCielo)

# ============= FUNDAMENTOS DE CREACIÓN 3D =============
# === MODELADO ===
    bpy.types.Scene.mostrar_modelado = bpy.props.BoolProperty(
        name="Fundamentos de Creación 3D",
        description="Despliega el árbol de habilidades centrado en técnicas fundamentales de creación 3D.",
        default=False
    )
    bpy.types.Scene.mostrar_manual_modelado = bpy.props.BoolProperty(
        name="Manual de Modelado",
        description="Muestra una guía educativa del dominio Modelado en Blender.",
        default=False
    )
    bpy.types.Scene.mostrar_retos_modelado = bpy.props.BoolProperty(
        name="Retos de Modelado",
        description="Muestra retos para desarrollar habilidades en modelado 3D.",
        default=False
    )
    bpy.types.Scene.retos_modelado = bpy.props.CollectionProperty(type=EscaleraItem)

# ============= DINÁMICA Y EXPRESIÓN =============
# === ANIMACIÓN ===
    bpy.types.Scene.mostrar_animacion = bpy.props.BoolProperty(
        name="Dinámica y Expresión",
        description="Despliega el árbol de habilidades enfocado en movimiento, actuación y expresividad en Blender.",
        default=False
    )
    bpy.types.Scene.mostrar_manual_animacion = bpy.props.BoolProperty(
        name="Manual de Conocimientos",
        description="Muestra un botón para abrir una guía externa .blend con contenidos teóricos y prácticos.",
        default=False
    )
    bpy.types.Scene.mostrar_retos_animacion = bpy.props.BoolProperty(
        name="Retos",
        description="Muestra una lista de ejercicios prácticos para afianzar habilidades específicas del dominio.",
        default=False
    )
    bpy.types.Scene.retos_animacion = bpy.props.CollectionProperty(type=EscaleraItem)

# ============= PRODUCCIÓN Y REFINAMIENTO =============
# === POSTPRODUCCIÓN ===
    bpy.types.Scene.mostrar_produccion = bpy.props.BoolProperty(
        name="Producción y Refinamiento",
        description="Despliega el árbol de habilidades enfocado en edición, refinamiento y finalización de proyectos.",
        default=False
    )
    bpy.types.Scene.mostrar_manual_postproduccion = bpy.props.BoolProperty(
        name="Manual de Conocimientos",
        description="Muestra un botón para abrir una guía externa .blend con contenidos de postproducción.",
        default=False
    )
    bpy.types.Scene.mostrar_retos_postproduccion = bpy.props.BoolProperty(
        name="Retos",
        description="Muestra una lista de retos para afianzar habilidades de postproducción.",
        default=False
    )
    bpy.types.Scene.retos_postproduccion = bpy.props.CollectionProperty(type=EscaleraItem)

#-------------------------------------------------------------------------------------------------------------

def unregister():
    bpy.utils.unregister_class(EscaleraItem)
    bpy.utils.unregister_class(ESCALERA_OT_AbrirBlendExterno)
    bpy.utils.unregister_class(ESCALERA_OT_CargarRetosModelado)
    bpy.utils.unregister_class(ESCALERA_OT_CargarRetosAnimacion)
    bpy.utils.unregister_class(ESCALERA_OT_CargarRetosPostProduccion)
    bpy.utils.unregister_class(PANEL_PT_EscaleraCielo)

# ============= FUNDAMENTOS DE CREACIÓN 3D =============
# === MODELADO ===
    del bpy.types.Scene.mostrar_modelado
    del bpy.types.Scene.mostrar_manual_modelado
    del bpy.types.Scene.mostrar_retos_modelado
    del bpy.types.Scene.retos_modelado

# ============= DINÁMICA Y EXPRESIÓN =============
# === ANIMACIÓN ===
    del bpy.types.Scene.mostrar_animacion
    del bpy.types.Scene.mostrar_manual_animacion
    del bpy.types.Scene.mostrar_retos_animacion
    del bpy.types.Scene.retos_animacion

# ============= PRODUCCIÓN Y REFINAMIENTO =============
# === POSTPRODUCCIÓN ===
    del bpy.types.Scene.mostrar_produccion
    del bpy.types.Scene.mostrar_manual_postproduccion
    del bpy.types.Scene.mostrar_retos_postproduccion
    del bpy.types.Scene.retos_postproduccion
