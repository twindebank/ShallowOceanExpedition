from random import choice


class Submarine:
    def __init__(self):
        self.value = None
        self.level = 'Submarine'

    def __repr__(self):
        return """Submarine"""


class TileStack:
    def __init__(self, tiles):
        self._tiles = tiles
        self.level = tuple(tile.level for tile in tiles)
        self.__value = None

    @property
    def value(self):
        if self.__value is None:
            self.__value = sum([tile.value for tile in self._tiles])
        return self.__value

    def __repr__(self):
        return f"""Level: {self.level}"""


class Tile:
    def __init__(self, level):
        self.level = level
        self.__value = None
        if level == 0:
            self.value_range = [0]
        elif level == 1:
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

    def __repr__(self):
        return f"""Level: {self.level}"""