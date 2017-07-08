import display
import layers
import typing
import entities
import size_constants


class MapDrawing(object):
    def __init__(self, content, display):
        self.display = display
        self.content = content
        self.map = content.map

    def execute_tick(self):
        self.draw_map()

    def draw_map(self):
        self.draw_map_layer(layers.TerrainLayer)

    def draw_map_layer(self, layer: typing.Type[layers.Layer]):
        for y in range(self.map.get_width()):
            for x in range(self.map.get_height()):
                self.draw_tile_layer(layer, x, y)

    def draw_tile_layer(self, layer: typing.Type[layers.Layer], x, y):
        entity = self.map.get_entities(layer, x, y)
        self.draw_entity(entity, x, y)

    def draw_entity(self, entity: entities.Entity, x, y):
        pass
        # sprite = entity.get_sprite()
        # if sprite:
        #     top_left_screen_tile_x = x + self.screenOffset_x - self.scrollOffset_x
        #     top_left_screen_tile_y = y + self.screenOffset_y - self.scrollOffset_y
        #
        #     self.display.blit()

