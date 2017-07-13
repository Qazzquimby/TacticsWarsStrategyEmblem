from display import Display
import layers
import typing
import entities
import point
import size_constants
import sprites


class MapDrawing(object):
    def __init__(self, content, display: Display):
        self.display = display  # type: Display
        self.content = content
        self.top_bar = self.content.top_bar
        self.map = content.map
        self.world_menu = content.world_menu

        self.map_larger_than_screen = self._init_map_larger_than_screen()
        self.map_center_offset = self._init_map_center_offset()

    def execute_tick(self):
        self.draw_top_bar()
        self.draw_map()
        self.draw_world_menu()

    def draw_top_bar(self):
        sprite = self.top_bar.sprite
        screen_tile = point.TilePoint(0, 0)
        screen_pixel = screen_tile.to_pixel_point()
        self.display.blit(sprite, screen_pixel)

    def draw_map(self):
        self.draw_map_layer(layers.TerrainLayer)
        self.draw_map_layer(layers.BuildingLayer)
        # todo other layers

    def draw_map_layer(self, layer: typing.Type[layers.Layer]):
        for y in range(self.map.width):
            for x in range(self.map.height):
                location = point.Location(x, y)
                self.draw_tile_layer(layer, location)

    def draw_tile_layer(self, layer: typing.Type[layers.Layer], location: point.Location):
        entity = self.map.get_entities(layer, location)
        self.draw_entity(entity, location)

    def draw_entity(self, entity: entities.Entity, location: point.Location):
        sprite = entity.sprite
        if sprite:
            screen_tile = point.TilePoint(location.x + self.map_center_offset.x,
                                          location.y + self.map_center_offset.y +
                                          size_constants.TOP_BAR_TILE_HEIGHT)

            screen_pixel = screen_tile.to_pixel_point()

            self.display.blit(sprite, screen_pixel)
        else:
            raise sprites.MissingSpriteException

    def draw_world_menu(self):
        sprite = self.world_menu.sprite
        menu_top_tile = size_constants.TOP_BAR_TILE_HEIGHT + size_constants.MAP_TILE_HEIGHT

        screen_tile = point.TilePoint(0, menu_top_tile)
        screen_pixel = screen_tile.to_pixel_point()

        self.display.blit(sprite, screen_pixel)

    def _init_map_larger_than_screen(self) -> bool:
        is_taller = self.map.height > size_constants.MAP_TILE_HEIGHT
        is_wider = self.map.width > size_constants.MAP_TILE_WIDTH
        is_larger = is_taller or is_wider
        return is_larger

    def _init_map_center_offset(self) -> point.PixelPoint:
        if self.map_larger_than_screen:
            return point.PixelPoint(0, 0)
        else:
            centered_x = int((size_constants.MAP_TILE_WIDTH - self.map.width) / 2)
            centered_y = int((size_constants.MAP_TILE_HEIGHT - self.map.height) / 2)
            return point.PixelPoint(centered_x, centered_y)
