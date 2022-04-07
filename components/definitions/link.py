import bpy
from bpy.props import StringProperty
from .hubs_component import HubsComponent
from ..types import Category, PanelType, NodeType


class hubs_component_link(HubsComponent):
    _definition = {
        'export_name': 'link',
        'display_name': 'Link',
        'category': Category.ELEMENTS,
        'node_type': NodeType.NODE,
        'pane_type': PanelType.OBJECT,
        'icon': 'link.png',
        'networked': True
    }

    href: StringProperty(name="URL", description="URL", default="https://")