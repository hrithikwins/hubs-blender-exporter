from ..types import Category, PanelType, NodeType
from ..hubs_component import HubsComponent
from bpy.props import CollectionProperty, StringProperty, EnumProperty, IntProperty
from bpy.types import PropertyGroup, Operator
import bpy

class SceneEventPropItem(PropertyGroup):
    name: StringProperty(name="Property", default="")
    value: StringProperty(name="Value", default="")

bpy.utils.register_class(SceneEventPropItem)


class AddSceneEventProp(Operator):
    bl_idname = "hubs.add_scene_event_prop"
    bl_label = "Add Scene Event Property"

    panel_type: StringProperty(name="panel_type")

    def execute(self, context):
        panel_type = PanelType(self.panel_type)
        ob = context.object
        host = ob if panel_type == PanelType.OBJECT else context.active_bone
        host.hubs_component_scene_event.additionalProps.add()
        return {'FINISHED'}


class RemoveSceneEventProp(Operator):
    bl_idname = "hubs.remove_scene_event_prop"
    bl_label = "Remove Scene Event Property"

    panel_type: StringProperty(name="panel_type")
    index: IntProperty()

    def execute(self, context):
        panel_type = PanelType(self.panel_type)
        ob = context.object
        host = ob if panel_type == PanelType.OBJECT else context.active_bone
        host.hubs_component_scene_event.additionalProps.remove(self.index)
        return {'FINISHED'}


class SceneEvent(HubsComponent):
    _definition = {
        'name': 'scene-event',
        'display_name': 'Scene Event',
        'category': Category.OBJECT,
        'node_type': NodeType.NODE,
        'panel_type': [PanelType.OBJECT, PanelType.BONE],
        'icon': 'MOUSE_LMB_DRAG',
        'version': (1, 0, 0)
    }
# event name: iframe_open | open_external_link | capture_screenshot | mute_microphone
# additional props : {url: "https://youtube.com/",type:"full",action: "close"}
    eventName: EnumProperty(
        name="Event Name",
        description="Event name in lower snake cake (example: iframe_open)",
        items=[
            ("iframe_open", "iframe_open", "iframe_open")
        ],
        default="iframe_open")

    additionalProps: CollectionProperty(type=SceneEventPropItem)

    # additionalProps: StringProperty(
    #     name="Additional Props",
    #     description="Use {} always to specify and should be valid JSON object (example: {url: \"https://youtube.com\"})",
    #     default="{url: 'https://youtube.com/embed/someid'}")


    @classmethod
    def init(cls, host):
        component = getattr(host, cls.get_id())
        prop = component.additionalProps.add()
        prop.name = "url"
        prop.value = "https://youtube.com/embed/someid"


    def draw(self, context, layout, panel):
        layout.prop(self, "eventName")
        box = layout.box()
        for i, prop in enumerate(self.additionalProps):
            row = box.row()
            row.prop(prop, "name")
            row.prop(prop, "value")
            op = row.operator(RemoveSceneEventProp.bl_idname, text="", icon="REMOVE")
            op.panel_type = panel.bl_context
            op.index = i

        op = box.operator(AddSceneEventProp.bl_idname, text="", icon="ADD")
        op.panel_type = panel.bl_context

    def gather(self, export_settings, object):
        scene_event_properties = {
            "eventName": self.eventName,
            "additionalProps": {}
            }
        for prop in self.additionalProps:
            scene_event_properties["additionalProps"][prop.name] = prop.value

        return scene_event_properties


    @staticmethod
    def register():
        bpy.utils.register_class(AddSceneEventProp)
        bpy.utils.register_class(RemoveSceneEventProp)


    @staticmethod
    def unregister():
        bpy.utils.unregister_class(SceneEventPropItem)
        bpy.utils.unregister_class(AddSceneEventProp)
        bpy.utils.unregister_class(RemoveSceneEventProp)



