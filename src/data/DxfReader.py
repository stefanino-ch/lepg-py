"""
:Author: Stefan Feuz; http://www.laboratoridenvol.com
:License: General Public License GNU GPL 3.0
"""

import ezdxf
import logging

from data.Entities3d import Line3D, Text3D, Circle3D


class DxfReader:
    """
    :class: Reads content from a DXF file
    """

    __className = 'DxfReader'
    '''
    :attr: Does help to indicate the source of the log messages
    '''

    def __init__(self):
        """
        :constructor:
        """
        self.doc = None

    def open_doc(self, doc_name):
        """
        :method: Opens a dxf file
        :param doc_name: fully qualified path& name of the file
        :retval: Reference to the document object
                 None if document can not be opened
        """
        if len(doc_name) == 0:
            return None

        try:
            self.doc = ezdxf.readfile(doc_name)
            return self.doc

        except IOError:
            logging.error(self.__className
                          + '.open_doc'
                          + 'Not a DXF file or a generic I/O error.')
            return None
        except ezdxf.DXFStructureError:
            logging.error(self.__className
                          + '.open_doc'
                          + 'Invalid or corrupted DXF file.')
            return None

    def read_layers_entities(self):
        """
        :method: Reads all layers and entity types from a dxf file
        :return: Dict, key= layer name, values= list with all entities found
                 in layer
        """
        inventory = {}
        entities_list = []

        msp = self.doc.modelspace()
        group = msp.groupby(dxfattrib="layer")

        for layer, entities in group.items():
            del entities_list[:]

            for entity in entities:
                dxf_type = entity.dxftype()

                if dxf_type == 'LINE':
                    line = Line3D(*entity.dxf.start,
                                  *entity.dxf.end,
                                  *ezdxf.colors.aci2rgb(entity.dxf.color))
                    entities_list.append(line)

                elif dxf_type == 'TEXT':
                    text = Text3D(*entity.dxf.insert,
                                  entity.dxf.text,
                                  entity.dxf.height,
                                  *ezdxf.colors.aci2rgb(entity.dxf.color),
                                  entity.dxf.rotation)
                    entities_list.append(text)

                elif dxf_type == 'CIRCLE':
                    circle = Circle3D(*entity.dxf.center,
                                      entity.dxf.radius,
                                      *ezdxf.colors.aci2rgb(entity.dxf.color))
                    entities_list.append(circle)
                else:
                    logging.info(self.__className
                                 + '.open_doc'
                                 + f'unknown element found: {dxf_type}')

            inventory[layer] = entities_list.copy()

        return inventory
