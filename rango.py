import bpy
from . import utils_json

CONFIG_FILE = "configuracion.json"

class PANEL_PT_Rango(bpy.types.Panel):
    bl_label = "Define tu Rango"
    bl_idname = "PANEL_PT_rango"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Gamification'

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        row = layout.row(align=True)
        row.label(text="Selecciona tu Nivel:")
        pin_icon = "PINNED" if scene.rango_fijado else "UNPINNED"
        row.operator("rango.toggle_fijar", text="", icon=pin_icon)

        col = layout.column(align=True)
        col.enabled = not scene.rango_fijado

        col.prop(scene, "nivel_usuario", expand=True)

        layout.operator("rango.guardar", text="Guardar Nivel", icon='CHECKMARK')
        layout.label(text=f"Nivel actual: {scene.nivel_usuario}", icon="INFO")


class RANGO_OT_Guardar(bpy.types.Operator):
    bl_idname = "rango.guardar"
    bl_label = "Guardar Nivel"
    bl_description = "Se guarda hasta que el usuario lo cambie manualmente."

    def execute(self, context):
        nivel = context.scene.nivel_usuario
        utils_json.guardar_json(CONFIG_FILE, {"nivel_usuario": nivel})
        self.report({'INFO'}, f"Nivel guardado: {nivel}")
        return {'FINISHED'}


class RANGO_OT_ToggleFijar(bpy.types.Operator):
    bl_idname = "rango.toggle_fijar"
    bl_label = "Fijar Nivel"
    bl_description = "Bloquea la selección de nivel antes de continuar para guardar la información."


    def execute(self, context):
        scene = context.scene
        scene.rango_fijado = not scene.rango_fijado
        return {'FINISHED'}


def register():
    bpy.utils.register_class(PANEL_PT_Rango)
    bpy.utils.register_class(RANGO_OT_Guardar)
    bpy.utils.register_class(RANGO_OT_ToggleFijar)

    bpy.types.Scene.nivel_usuario = bpy.props.EnumProperty(
        name="Rango",
        description="Define tu nivel",
        items=[
            ("Novato", "🟢 Novato", ""),
            ("Aprendiz", "🔵 Aprendiz", ""),
            ("Experto", "🟠 Experto", ""),
            ("Maestro", "🔴 Maestro", ""),
        ],
        default="Novato"
    )

    bpy.types.Scene.rango_fijado = bpy.props.BoolProperty(
        name="Rango Fijado",
        description="Evita cambiar el nivel una vez fijado",
        default=False
    )


def unregister():
    bpy.utils.unregister_class(PANEL_PT_Rango)
    bpy.utils.unregister_class(RANGO_OT_Guardar)
    bpy.utils.unregister_class(RANGO_OT_ToggleFijar)
    del bpy.types.Scene.nivel_usuario
    del bpy.types.Scene.rango_fijado
