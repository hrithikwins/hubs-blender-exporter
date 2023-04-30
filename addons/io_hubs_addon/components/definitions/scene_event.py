from ..models import spawn_point
from ..gizmos import CustomModelGizmo, bone_matrix_world
from ..types import Category, PanelType, NodeType
from ..hubs_component import HubsComponent
from bpy.props import BoolProperty, StringProperty
from .networked import migrate_networked


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
    eventName: StringProperty(
        name="Event Name",
        description="Event name in lower snake cake (example: iframe_open)",
        default="iframe_open")

    additionalProps: StringProperty(
        name="Additional Props",
        description="Use {} always to specify and should be valid JSON object (example: {url: \"https://youtube.com\"})",
        default="{url: 'https://youtube.com/embed/someid'}")



