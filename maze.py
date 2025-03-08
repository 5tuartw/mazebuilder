import random
import time
from cell import Cell
from collections import deque

class Maze():
  def __init__(
    self,
    x1,
    y1,
    num_rows,
    num_cols,
    cell_size_x,
    cell_size_y,
    win=None,
    canvas=None,
    seed=None,
    style=None
  ):
    self._x1 = x1
    self._y1 = y1
    self._num_rows = num_rows
    self._num_cols = num_cols
    self._cell_size_x = cell_size_x
    self._cell_size_y = cell_size_y
    self._win = win
    self._canvas = canvas
    if seed:
      random.seed(seed)
    self._cells = []
    self._visit_count = 0
    self._exit_found = False
    self._style = style
    self._shortest_path = []
    self._max_distance_to_path = 0
    
    self._create_cells()
    self._break_entrance_and_exit()
    if self._style == "Backtrack":
      self._break_walls_backtracking_r(0,0)
    if self._style == "Prim's":
      self._break_walls_prims()
    if self._style == "Kruskal's":
      self._break_walls_kruskal()
    self.colour_paths()
    self._reset_cells_visited()

  def _create_cells(self):
    #self._canvas.delete("all")
    for column in range(self._num_cols):
      this_column = []
      for row in range(self._num_rows):
        this_column.append(Cell(self._canvas))
      self._cells.append(this_column)

    for i in range(self._num_cols):
      for j in range(self._num_rows):
        self._draw_cell(i,j)

  def _draw_cell(self, i, j):
    if self._win is None:
      return
    x1 = self._x1 + i * self._cell_size_x
    y1 = self._y1 + j * self._cell_size_y
    x2 = x1 + self._cell_size_x
    y2 = y1 + self._cell_size_y
    self._cells[i][j].draw(x1,y1,x2,y2)
    self._animate()

  def _animate(self):
    if self._canvas is None:
      return
    self._canvas.update()
    base_delay = 0.001
    scale_factor = (self._num_cols * self._num_rows / 100)
    delay = max (0.001, min(base_delay, base_delay / scale_factor))
    time.sleep(delay)

  def _break_entrance_and_exit(self):
    self._cells[0][0].has_top_wall = False
    self._draw_cell(0,0)
    self._cells[self._num_cols-1][self._num_rows-1].has_bottom_wall = False
    self._draw_cell(self._num_cols-1, self._num_rows-1)
  

  # recursive backtracking algorithm for maze generation
  # starts with cell i, j and moves to a random unvisited neighbour, removing walls in between them
  # if no unvisited neighbours, backtracks to the previous cell
  def _break_walls_backtracking_r(self, i, j):
    self._cells[i][j].visited = True
    while True:
      to_visit = []

      #try left
      if i > 0 and not self._cells[i-1][j].visited:
        to_visit.append((i-1,j))
      #try right
      if i < self._num_cols-1 and not self._cells[i+1][j].visited:
        to_visit.append((i+1,j))
      #try up
      if j > 0 and not self._cells[i][j-1].visited:
        to_visit.append((i,j-1))
      #try down
      if j < self._num_rows-1 and not self._cells[i][j+1].visited:
        to_visit.append((i,j+1))

      if len(to_visit) == 0:
        self._draw_cell(i,j)
        return

      rand_dir = random.randrange(len(to_visit))
      next_cell = to_visit[rand_dir]

      #left
      if next_cell[0] == i - 1:
        self._cells[i][j].has_left_wall = False
        self._cells[i-1][j].has_right_wall = False
      #right
      if next_cell[0] == i + 1:
        self._cells[i][j].has_right_wall = False
        self._cells[i+1][j].has_left_wall = False
      #up
      if next_cell[1] == j - 1:
        self._cells[i][j].has_top_wall = False
        self._cells[i][j-1].has_bottom_wall = False
      #down
      if next_cell[1] == j + 1:
        self._cells[i][j].has_bottom_wall = False
        self._cells[i][j+1].has_top_wall = False
      
      #time.sleep(0.4)
      self._break_walls_backtracking_r(next_cell[0], next_cell[1])


  # Prim's algorithm for maze generation
  # Starts with a random cell and adds all walls to a list
  # Randomly selects a wall from the list and removes it if one cell is visited and the other is not
  # Adds the new cell to the list of visited cells and adds all walls of the new cell to the list
  # Repeats until all cells are visited
  def _break_walls_prims(self):
    start_x = random.randrange(self._num_cols)
    start_y = random.randrange(self._num_rows)
    self._cells[start_x][start_y].visited = True
    walls = []
    #add all walls to the list
    for i in range(self._num_cols):
      for j in range(self._num_rows):
        if i > 0:
          walls.append((i,j,i-1,j))
        if i < self._num_cols - 1:
          walls.append((i,j,i+1,j))
        if j > 0:
          walls.append((i,j,i,j-1))
        if j < self._num_rows - 1:
          walls.append((i,j,i,j+1))
    while len(walls) > 0:
      random.shuffle(walls)
      wall = walls.pop()
      x1 = wall[0]
      y1 = wall[1]
      x2 = wall[2]
      y2 = wall[3]
      if self._cells[x1][y1].visited and not self._cells[x2][y2].visited:
        # Remove the wall between the cells
        if x1 == x2:
            if y1 > y2:
                self._cells[x1][y1].has_top_wall = False
                self._cells[x2][y2].has_bottom_wall = False
            else:
                self._cells[x1][y1].has_bottom_wall = False
                self._cells[x2][y2].has_top_wall = False
        else:
            if x1 > x2:
                self._cells[x1][y1].has_left_wall = False
                self._cells[x2][y2].has_right_wall = False
            else:
                self._cells[x1][y1].has_right_wall = False
                self._cells[x2][y2].has_left_wall = False
        self._cells[x2][y2].visited = True
        self._draw_cell(x1, y1)
        self._draw_cell(x2, y2)
        self._animate()

        #add new walls to the list
        if x2 > 0:
          walls.append((x2,y2,x2-1,y2))
        if x2 < self._num_cols - 1:
          walls.append((x2,y2,x2+1,y2))
        if y2 > 0:
          walls.append((x2,y2,x2,y2-1))
        if y2 < self._num_rows - 1:
          walls.append((x2,y2,x2,y2+1))
        self._animate()

    self._reset_cells_visited()

  # Kruskal's method ensure's that any two points only have 1 path between them
  # Each cell starts as its own independent set
  # It randomly chooses the walls of a cell to break and merge its set with the new join
  # This repeats until there is only one set
  # The maze becomes a random spanning tree, a connected graph without cycles
  def _break_walls_kruskal(self):
    walls = []
    sets = {}
    for i in range(self._num_cols):
        for j in range(self._num_rows):
            sets[(i, j)] = (i, j)
            if i > 0:
                walls.append((i, j, i-1, j))
            if j > 0:
                walls.append((i, j, i, j-1))

    def find(cell):
        if sets[cell] != cell:
            sets[cell] = find(sets[cell])
        return sets[cell]

    def union(cell1, cell2):
        root1 = find(cell1)
        root2 = find(cell2)
        if root1 != root2:
            sets[root2] = root1

    random.shuffle(walls)
    for wall in walls:
        x1, y1, x2, y2 = wall
        if find((x1, y1)) != find((x2, y2)):
            if x1 == x2:
                if y1 > y2:
                    self._cells[x1][y1].has_top_wall = False
                    self._cells[x2][y2].has_bottom_wall = False
                else:
                    self._cells[x1][y1].has_bottom_wall = False
                    self._cells[x2][y2].has_top_wall = False
            else:
                if x1 > x2:
                    self._cells[x1][y1].has_left_wall = False
                    self._cells[x2][y2].has_right_wall = False
                else:
                    self._cells[x1][y1].has_right_wall = False
                    self._cells[x2][y2].has_left_wall = False
            union((x1, y1), (x2, y2))
            self._draw_cell(x1, y1)
            self._draw_cell(x2, y2)
            self._animate()

    self._reset_cells_visited()

  # resets all cells' visited varialbe to False to reenable searching/checking
  def _reset_cells_visited(self):
    self._visit_count = 0
    for i in self._cells:
      for j in i:
        j.visited = False

  # calls _solve_r recursive function starting from the bottom right cell
  def solve(self):
    return self._solve_r(self._num_cols-1, self._num_rows-1)
  
  def _solve_r(self, i, j):
    self._animate()
    self._cells[i][j].visited = True
    self._visit_count += 1
    if i == 0 and j == 0:
      self._exit_found = True
    if self._visit_count == self._num_cols * self._num_rows:
      return True
    
    #try left
    if i > 0 and not self._cells[i][j].has_left_wall and not self._cells[i-1][j].visited:
      self._cells[i][j].draw_move(self._cells[i-1][j])
      if self._solve_r(i-1,j):
        return True
      else:
        self._cells[i][j].draw_move(self._cells[i-1][j],not self._exit_found)
    
    #try right
    if i < self._num_cols - 1 and not self._cells[i][j].has_right_wall and not self._cells[i+1][j].visited:
      self._cells[i][j].draw_move(self._cells[i+1][j])
      if self._solve_r(i+1,j):
        return True
      else:
        self._cells[i][j].draw_move(self._cells[i+1][j],not self._exit_found)

    #try up
    if j > 0 and not self._cells[i][j].has_top_wall and not self._cells[i][j-1].visited:
      self._cells[i][j].draw_move(self._cells[i][j-1])
      if self._solve_r(i,j-1):
        return True
      else:
        self._cells[i][j].draw_move(self._cells[i][j-1],not self._exit_found)
    #try down
    if j < self._num_rows - 1 and not self._cells[i][j].has_bottom_wall and not self._cells[i][j+1].visited:
      self._cells[i][j].draw_move(self._cells[i][j+1])
      if self._solve_r(i,j+1):
        return True
      else:
        self._cells[i][j].draw_move(self._cells[i][j+1],not self._exit_found)
    
    return False
  
  # breadth-first-search to 
  def find_shortest_path(self, start, end):
      queue = deque([(start, [start])])
      visited = set()
      while queue:
          (current, path) = queue.popleft()
          if current == end:
              return path
          visited.add(current)
          i, j = current
          neighbors = []
          if i > 0 and not self._cells[i][j].has_left_wall:
              neighbors.append((i-1, j))
          if i < self._num_cols - 1 and not self._cells[i][j].has_right_wall:
              neighbors.append((i+1, j))
          if j > 0 and not self._cells[i][j].has_top_wall:
              neighbors.append((i, j-1))
          if j < self._num_rows - 1 and not self._cells[i][j].has_bottom_wall:
              neighbors.append((i, j+1))
          for neighbor in neighbors:
              if neighbor not in visited:
                  queue.append((neighbor, path + [neighbor]))
      return None

  def draw_shortest_path(self):
      if self._shortest_path:
              pi = None
              pj = None
      for i, j in self._shortest_path:
          if pi is not None:
              self._cells[pi][pj].draw_move(self._cells[i][j])
          pi = i
          pj = j
          self._animate()

  def update_distances_to_path(self):

      # 1. Find cells on the shortest path with branches
      branching_cells = []
      for i, j in self._shortest_path:
          neighbors = []
          if i > 0 and not self._cells[i][j].has_left_wall:
              neighbors.append((i - 1, j))
          if i < self._num_cols - 1 and not self._cells[i][j].has_right_wall:
              neighbors.append((i + 1, j))
          if j > 0 and not self._cells[i][j].has_top_wall:
              neighbors.append((i, j - 1))
          if j < self._num_rows - 1 and not self._cells[i][j].has_bottom_wall:
              neighbors.append((i, j + 1))

          # Check if there's a neighbor not on the shortest path
          for ni, nj in neighbors:
              if (ni, nj) not in self._shortest_path:
                  branching_cells.append((i, j))
                  break  # Move on to the next cell in the shortest path

      # 2. Initialize distances for cells on the shortest path
      for i, j in self._shortest_path:
          self._cells[i][j].distance_to_path = 0

      # 3. Calculate distances for branching cells and their neighbors
      distance = 1
      current_level = branching_cells  # Start with the branching cells
      while current_level:
          next_level = []
          for i, j in current_level:
              neighbors = []
              if i > 0 and not self._cells[i][j].has_left_wall:
                  neighbors.append((i - 1, j))
              if i < self._num_cols - 1 and not self._cells[i][j].has_right_wall:
                  neighbors.append((i + 1, j))
              if j > 0 and not self._cells[i][j].has_top_wall:
                  neighbors.append((i, j - 1))
              if j < self._num_rows - 1 and not self._cells[i][j].has_bottom_wall:
                  neighbors.append((i, j + 1))

              for ni, nj in neighbors:
                  if self._cells[ni][nj].distance_to_path is None:
                      self._cells[ni][nj].distance_to_path = distance
                      self._max_distance_to_path = max(self._max_distance_to_path, distance)
                      next_level.append((ni, nj))

          current_level = next_level  # Move to the next level of branching
          distance += 1

  # Looks at cells not on the past and calculate's their distance, colouring them on a
  # gradient from yellow (on the route) to red (farthest from shortest route)
  def colour_paths(self):
      start = (0, 0)
      end = (self._num_cols - 1, self._num_rows - 1)
      self._shortest_path = self.find_shortest_path(start, end)
      self.update_distances_to_path()

      if self._shortest_path:
          # longest path variable deprecated due to making it difficult to compare mazes objectively
          # longest_path = self._num_cols * self._num_rows - len(self._shortest_path)
          for i in range(self._num_cols):
              for j in range(self._num_rows):
                  distance = self._cells[i][j].distance_to_path
                  if distance is not None:
                      # Calculate the color based on the distance
                      if distance == 0:
                          color = '#FFFF00'  # Yellow
                      else:
                          red_intensity = 255
                          green_intensity = int(255 * (1 - (distance / len(self._shortest_path))))
                          green_intensity = max(0, min(255, green_intensity))  # Ensure green_intensity is within 0-255
                          color = f'#{red_intensity:02x}{green_intensity:02x}00'
                      self._cells[i][j].draw(self._x1 + i * self._cell_size_x, self._y1 + j * self._cell_size_y, self._x1 + (i+1) * self._cell_size_x, self._y1 + (j+1) * self._cell_size_y, colour=color)
                      self._animate()
  
  
