from random import choice


class Home:
    def __init__(self):
        self.value = None
        self.level = 'Home'


class Tile:
    def __init__(self, level):
        """
        properties:
            level (tuple): level of the tile
        """
        self.level = level,
        self.__value = None
        if level == 1:
            self.value_range = range(0, 5)
        elif level == 2:
            self.value_range = range(5, 10)
        elif level == 3:
            self.value_range = range(10, 15)
        elif level == 4:
            self.value_range = range(15, 20)
        else:
            raise ValueError('Level must be one of [1,2,3,4]')

    @property
    def value(self):
        if self.__value is None:
            self.__value = choice(self.value_range)
        return self.__value


class BlankTile:
    level = None
    @property
    def value(self):
        raise ValueError("Blank tile has no value.")


class TileStack:
    def __init__(self, tiles):
        if not tiles:
            raise ValueError("No tiles given.")
        self._tiles = tiles
        level = []
        for tile in tiles:
            level.extend(tile.level)
        self.level = tuple(level)
        self.__value = None

    @property
    def value(self):
        if self.__value is None:
            self.__value = sum([tile.value for tile in self._tiles])
        return self.__value
