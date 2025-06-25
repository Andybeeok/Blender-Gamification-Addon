import bpy
from . import utils_json
from difflib import get_close_matches

CONFIG_FILE = "configuracion.json"
TAREAS_FILE = "tareas.json"

class PANEL_PT_HojaRuta(bpy.types.Panel):
    bl_label = "La Hoja de Ruta"
    bl_idname = "PANEL_PT_hoja_ruta"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Gamification'

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.label(text="Escribe aquí tu Objetivo Principal")
        row = layout.row(align=True)
        row.prop(scene, "objetivo_principal")
        row.operator("hojaruta.reset_principal", text="", icon='LOOP_BACK')

        layout.label(text="Escribe aquí tu Objetivo Específico")
        row = layout.row(align=True)
        row.prop(scene, "objetivo_especifico")
        row.operator("hojaruta.reset_especifico", text="", icon='LOOP_BACK')

        layout.operator("hojaruta.analizar", text="Analizar Objetivos", icon='VIEWZOOM')


class HOJARUTA_OT_ResetPrincipal(bpy.types.Operator):
    bl_idname = "hojaruta.reset_principal"
    bl_label = "Restaurar Objetivo Principal"
    bl_description = "Borrar campo de Texto"


    def execute(self, context):
        context.scene.objetivo_principal = ""
        return {'FINISHED'}


class HOJARUTA_OT_ResetEspecifico(bpy.types.Operator):
    bl_idname = "hojaruta.reset_especifico"
    bl_label = "Restaurar Objetivo Específico"
    bl_description = "Borrar campo de Texto"

    def execute(self, context):
        context.scene.objetivo_especifico = ""
        return {'FINISHED'}


class HOJARUTA_OT_AnalizarObjetivos(bpy.types.Operator):
    bl_idname = "hojaruta.analizar"
    bl_label = "Analizar Objetivos"
    bl_description = "Analiza los objetivos para generar Hábitos y Tareas personalizadas."


    def execute(self, context):
        scene = context.scene
        texto_completo = f"{scene.objetivo_principal} {scene.objetivo_especifico}".lower()
        palabras_objetivo = texto_completo.split()

        datos = utils_json.cargar_json(TAREAS_FILE)
        nivel = utils_json.cargar_json(CONFIG_FILE).get("nivel_usuario", "Novato")

        dominios_encontrados = set()

        for dominio, contenido in datos.get(nivel, {}).items():
            palabras_clave = contenido.get("keywords", [])
            for palabra in palabras_objetivo:
                coincidencias = get_close_matches(palabra, palabras_clave, n=1, cutoff=0.6)
                if coincidencias:
                    dominios_encontrados.add(dominio)

        if dominios_encontrados:
            scene.hoja_habitos.clear()
            scene.hoja_tareas.clear()

            habitos_agregados = set()
            tareas_agregadas = set()

            for dominio in dominios_encontrados:
                grupo = datos[nivel].get(dominio, {})
                for habito in grupo.get("habitos", []):
                    if habito not in habitos_agregados:
                        item = scene.hoja_habitos.add()
                        item.name = habito
                        habitos_agregados.add(habito)
                for tarea in grupo.get("tareas", []):
                    if tarea not in tareas_agregadas:
                        item = scene.hoja_tareas.add()
                        item.name = tarea
                        tareas_agregadas.add(tarea)

            self.report({'INFO'}, f"Sugerencias de: {', '.join(dominios_encontrados)}")
        else:
            self.report({'WARNING'}, "No se encontraron sugerencias.")
            scene.hoja_habitos.clear()
            scene.hoja_tareas.clear()

        return {'FINISHED'}


class HojaRutaItem(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="Nombre")


def register():
    bpy.utils.register_class(PANEL_PT_HojaRuta)
    bpy.utils.register_class(HOJARUTA_OT_ResetPrincipal)
    bpy.utils.register_class(HOJARUTA_OT_ResetEspecifico)
    bpy.utils.register_class(HOJARUTA_OT_AnalizarObjetivos)
    bpy.utils.register_class(HojaRutaItem)

    bpy.types.Scene.objetivo_principal = bpy.props.StringProperty(name="")
    bpy.types.Scene.objetivo_especifico = bpy.props.StringProperty(name="")
    bpy.types.Scene.hoja_habitos = bpy.props.CollectionProperty(type=HojaRutaItem)
    bpy.types.Scene.hoja_tareas = bpy.props.CollectionProperty(type=HojaRutaItem)


def unregister():
    bpy.utils.unregister_class(PANEL_PT_HojaRuta)
    bpy.utils.unregister_class(HOJARUTA_OT_ResetPrincipal)
    bpy.utils.unregister_class(HOJARUTA_OT_ResetEspecifico)
    bpy.utils.unregister_class(HOJARUTA_OT_AnalizarObjetivos)
    bpy.utils.unregister_class(HojaRutaItem)

    del bpy.types.Scene.objetivo_principal
    del bpy.types.Scene.objetivo_especifico
    del bpy.types.Scene.hoja_habitos
    del bpy.types.Scene.hoja_tareas
