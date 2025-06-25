import bpy
from . import utils_json

HISTORIAL_FILE = "historial.json"

class MapaItem(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="Nombre")
    checked: bpy.props.BoolProperty(name="Completado", default=False)

class MetaItem(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="Meta")
    fecha: bpy.props.StringProperty(name="Fecha")
    checked: bpy.props.BoolProperty(name="Completada", default=False)

class MAPA_OT_SiguienteHabito(bpy.types.Operator):
    bl_idname = "mapa.siguiente_habito"
    bl_label = "Siguiente Hábito"
    bl_description = "Pasa al siguiente Hábito."

    def execute(self, context):
        scene = context.scene
        if scene.hoja_habitos:
            scene.indice_habito = (scene.indice_habito + 1) % len(scene.hoja_habitos)
        return {'FINISHED'}

class MAPA_OT_SiguienteTarea(bpy.types.Operator):
    bl_idname = "mapa.siguiente_tarea"
    bl_label = "Siguiente Tarea"
    bl_description = "Pasa a la siguiente Tarea."

    def execute(self, context):
        scene = context.scene
        if scene.hoja_tareas:
            scene.indice_tarea = (scene.indice_tarea + 1) % len(scene.hoja_tareas)
        return {'FINISHED'}

class MAPA_OT_GuardarMeta(bpy.types.Operator):
    bl_idname = "mapa.guardar_meta"
    bl_label = "Guardar Meta"
    bl_description = "Guarda tus Metas para poder registrar tus avances y marcar tus logros."


    def execute(self, context):
        scene = context.scene
        nueva = scene.metas_guardadas.add()
        nueva.name = scene.nueva_meta
        nueva.fecha = scene.fecha_meta
        scene.nueva_meta = ""
        scene.fecha_meta = ""
        return {'FINISHED'}

class MAPA_OT_MarcarMetaCompleta(bpy.types.Operator):
    bl_idname = "mapa.meta_completada"
    bl_label = "Marcar como Completada"
    bl_description = "Elimina esta Meta completada."


    index: bpy.props.IntProperty()

    def execute(self, context):
        scene = context.scene
        item = scene.metas_guardadas[self.index]
        historial = utils_json.cargar_json(HISTORIAL_FILE)
        if "metas_completadas" not in historial:
            historial["metas_completadas"] = []
        historial["metas_completadas"].append({"meta": item.name, "fecha": item.fecha})
        utils_json.guardar_json(HISTORIAL_FILE, historial)
        scene.metas_guardadas.remove(self.index)
        return {'FINISHED'}

class MAPA_OT_LimpiarTodo(bpy.types.Operator):
    bl_idname = "mapa.limpiar_todo"
    bl_label = "Limpiar Todo"
    bl_description = "Borra todos los Hábitos, Tareas y Metas generadas en El Mapa del Aventurero."

    def execute(self, context):
        scene = context.scene
        scene.hoja_habitos.clear()
        scene.hoja_tareas.clear()
        scene.metas_guardadas.clear()
        scene.indice_habito = 0
        scene.indice_tarea = 0
        scene.nueva_meta = ""
        scene.fecha_meta = ""
        utils_json.guardar_json(HISTORIAL_FILE, {})
        self.report({'INFO'}, "Todos los datos fueron reiniciados.")
        return {'FINISHED'}

class PANEL_PT_MapaAventurero(bpy.types.Panel):
    bl_label = "El Mapa del Aventurero"
    bl_idname = "PANEL_PT_mapa_aventurero"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Gamification'

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.label(text=f"Nivel Actual: {scene.nivel_actual}")

        box_hab = layout.box()
        row = box_hab.row()
        row.prop(scene, "mostrar_habitos", toggle=True, text="Hábitos", emboss=True)
        if scene.mostrar_habitos and scene.hoja_habitos:
            item = scene.hoja_habitos[scene.indice_habito % len(scene.hoja_habitos)]
            row = box_hab.row()
            row.prop(item, "checked", text=item.name)
            box_hab.operator("mapa.siguiente_habito", text="➡")

        box_tar = layout.box()
        row = box_tar.row()
        row.prop(scene, "mostrar_tareas", toggle=True, text="Tareas", emboss=True)
        if scene.mostrar_tareas and scene.hoja_tareas:
            item = scene.hoja_tareas[scene.indice_tarea % len(scene.hoja_tareas)]
            row = box_tar.row()
            row.prop(item, "checked", text=item.name)
            box_tar.operator("mapa.siguiente_tarea", text="➡")

        box_met = layout.box()
        row = box_met.row()
        row.prop(scene, "mostrar_metas", toggle=True, text="Metas", emboss=True)

        if scene.mostrar_metas:
            layout.prop(scene, "nueva_meta", text="Meta", icon='CURVE_PATH')
            layout.prop(scene, "fecha_meta", text="Fecha límite", icon='TIME')
            layout.operator("mapa.guardar_meta", text="Guardar Meta", icon='LAYER_ACTIVE')

            layout.label(text="Metas Pendientes:")
            for i, item in enumerate(scene.metas_guardadas):
                row = layout.row()
                row.prop(item, "checked", text=f"{item.name} - {item.fecha}")
                op = row.operator("mapa.meta_completada", text="", icon="CHECKMARK")
                op.index = i

        layout.separator()
        layout.operator("mapa.limpiar_todo", text="Limpiar Todo", icon='TRASH')

def register():
    bpy.utils.register_class(PANEL_PT_MapaAventurero)
    bpy.utils.register_class(MAPA_OT_GuardarMeta)
    bpy.utils.register_class(MAPA_OT_SiguienteHabito)
    bpy.utils.register_class(MAPA_OT_SiguienteTarea)
    bpy.utils.register_class(MAPA_OT_MarcarMetaCompleta)
    bpy.utils.register_class(MAPA_OT_LimpiarTodo)
    bpy.utils.register_class(MapaItem)
    bpy.utils.register_class(MetaItem)

    bpy.types.Scene.nivel_actual = bpy.props.StringProperty(name="Nivel Actual", default="No definido")
    bpy.types.Scene.indice_habito = bpy.props.IntProperty(name="Índice Hábito", default=0)
    bpy.types.Scene.indice_tarea = bpy.props.IntProperty(name="Índice Tarea", default=0)
    bpy.types.Scene.hoja_habitos = bpy.props.CollectionProperty(type=MapaItem)
    bpy.types.Scene.hoja_tareas = bpy.props.CollectionProperty(type=MapaItem)
    bpy.types.Scene.metas_guardadas = bpy.props.CollectionProperty(type=MetaItem)
    bpy.types.Scene.nueva_meta = bpy.props.StringProperty(name="Meta")
    bpy.types.Scene.fecha_meta = bpy.props.StringProperty(name="DeadLine")
    bpy.types.Scene.mostrar_habitos = bpy.props.BoolProperty(name="Mostrar Hábitos", default=False)
    bpy.types.Scene.mostrar_tareas = bpy.props.BoolProperty(name="Mostrar Tareas", default=False)
    bpy.types.Scene.mostrar_metas = bpy.props.BoolProperty(name="Mostrar Metas", default=False)

def unregister():
    bpy.utils.unregister_class(PANEL_PT_MapaAventurero)
    bpy.utils.unregister_class(MAPA_OT_GuardarMeta)
    bpy.utils.unregister_class(MAPA_OT_SiguienteHabito)
    bpy.utils.unregister_class(MAPA_OT_SiguienteTarea)
    bpy.utils.unregister_class(MAPA_OT_MarcarMetaCompleta)
    bpy.utils.unregister_class(MAPA_OT_LimpiarTodo)
    bpy.utils.unregister_class(MapaItem)
    bpy.utils.unregister_class(MetaItem)

    del bpy.types.Scene.nivel_actual
    del bpy.types.Scene.indice_habito
    del bpy.types.Scene.indice_tarea
    del bpy.types.Scene.hoja_habitos
    del bpy.types.Scene.hoja_tareas
    del bpy.types.Scene.metas_guardadas
    del bpy.types.Scene.nueva_meta
    del bpy.types.Scene.fecha_meta
    del bpy.types.Scene.mostrar_habitos
    del bpy.types.Scene.mostrar_tareas
    del bpy.types.Scene.mostrar_metas
