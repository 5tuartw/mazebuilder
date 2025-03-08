# dormant code for powerups in a playable version of the game

class Powerup:
    def __init__(self, canvas, cell_size, start_x, start_y, margin, item_type):
        self._canvas = canvas
        self._cell_size = cell_size
        self._x = start_x
        self._y = start_y
        self._margin = margin
        self._item_type = item_type
        self._player_size = cell_size // 1.5
        self._shape = None
        self._create_shape()
    
    def _create_shape(self):
        # calculate centre of the cell
        centre_x = self._margin + (self._x * self._cell_size) + (self._cell_size // 2)
        centre_y = self._margin + (self._y * self._cell_size) + (self._cell_size // 2)

        # calculate player bounds from centre
        radius = self._player_size // 2
        x1 = centre_x - radius
        y1 = centre_y - radius
        x2 = centre_x + radius
        y2 = centre_y + radius
        offset = self._cell_size

        if self._item_type == "invisibility":
            self._shape = self._canvas.create_arc(x1, y1, x2, y2, start = 100, extent = 45, outline = '#769aad', width = 0, fill = "#e8b82a")