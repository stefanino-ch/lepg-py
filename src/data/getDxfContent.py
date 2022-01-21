
import ezdxf
from Line3d import Line3D


class DxfReader:
    """
    :class: Reads content from a DXF file
    """
    def __init__(self):
        self.doc = None

    def open_doc(self, doc_name):
        if len(doc_name) == 0:
            return None

        try:
            self.doc = ezdxf.readfile(doc_name)
            return self.doc

        except IOError:
            print(f"Not a DXF file or a generic I/O error.")
            # sys.exit(1)
            return None
        except ezdxf.DXFStructureError:
            print(f"Invalid or corrupted DXF file.")
            # sys.exit(2)
            return None

    def get_layer_list(self):
        """
        :method: Reads all layers from the dxf file
        :return: List containing all layer names
        """
        layer_list = []

        for layer in self.doc.layers:
            layer_name = layer.dxf.name
            if layer_name not in layer_list:
                layer_list.append(layer_name)

        return layer_list

    def read_layers_entities_distinct(self):
        """
        :method: Reads all layers and entity types from a dxf file
        :return: Dict, key= layer name, values= list with entity types found
                 in layer
        """
        inventory = {}
        entities_distinct = []

        msp = self.doc.modelspace()
        group = msp.groupby(dxfattrib="layer")

        for layer, entities in group.items():
            del entities_distinct[:]

            for entity in entities:
                dxftype = entity.dxftype()

                if dxftype not in entities_distinct:
                    entities_distinct.append(dxftype)

            inventory[layer] = entities_distinct.copy()

        return inventory

    def print_inventory_distinct(self, inventory):
        """
        :method: Prints a inventory dict

        :param inventory: Dict with
                          key= layer name,
                          values= list with entity types found
        :return: n/a
        """
        keys = inventory.keys()

        for key in keys:
            print(f'Layer: {key}')
            entities = inventory.get(key)

            for entity in entities:
                print(f'\t{entity}')

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
                                  entity.dxf.color)
                    entities_list.append(line)
                else:
                    print(f'unknown element found: {dxf_type}')

            inventory[layer] = entities_list.copy()

        return inventory

    def print_inventory(self, inventory):
        """
        :method: Prints an inventory dict

        :param inventory: Dict with
                          key= layer name,
                          values= list with entity types found
        :return: n/a
        """
        keys = inventory.keys()

        for key in keys:
            print(f'Layer: {key}')
            entities = inventory.get(key)

            for entity in entities:
                if type(entity) is Line3D:
                    print(f'\tLine '
                          f'S: {entity.start.x3d, entity.start.y3d, entity.start.z3d}')


if __name__ == '__main__':
    print('start reading...')

    dxf_reader = DxfReader()
    dxf_doc = dxf_reader.open_doc("geometry.dxf")
    # dxf_doc = dxf_reader.open_doc("leparagliding.dxf")
    # dxf_doc = dxf_reader.open_doc("lep-3d.dxf")

    if dxf_doc:
        # inv = dxf_reader.read_layers_entities_distinct()
        # dxf_reader.print_inventory_distinct(inv)

        inv = dxf_reader.read_layers_entities()
        dxf_reader.print_inventory(inv)

    print('...done')
