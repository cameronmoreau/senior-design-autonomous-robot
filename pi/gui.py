import tkinter as tk
from game_manager import *

class GuiApplication(tk.Frame):
  def __init__(self, master=None, game_manager=None):
    super().__init__(master)

    self.game = game_manager

    self.create_widgets()
    self.setup_canvas()
    self.pack()

    # Lift frame to top
    master.lift()
    master.call('wm', 'attributes', '.', '-topmost', True)
    master.after_idle(master.call, 'wm', 'attributes', '.', '-topmost', False)

  def create_widgets(self):
    self.next_button = tk.Button(self, text="Next Round", command=self.next_round_pressed)
    self.next_button.pack()

    # Setup round
    self.round_label = tk.Label(self)
    self.round_label.pack()

    # Setup colors
    self.colors_label = tk.Label(self)
    self.colors_label.pack()

    self.update_widgets()

  def update_widgets(self):
    current_round = self.game.get_current_round()
    self.round_label["text"] = "ROUND: " + current_round.title
    self.colors_label["text"] = "COLORS: (Total: %s) %s" % (current_round.get_total_coins(), str(current_round.coins))

  def next_round_pressed(self):
    self.game.next_round()
    self.update_widgets()

  def setup_canvas(self):
    CELL_COUNT = 16
    BOX_SIZE = 16
    GRID_SIZE = 800
    CELL_SIZE = GRID_SIZE / CELL_COUNT
    self.canvas = tk.Canvas(self, width=GRID_SIZE, height=GRID_SIZE)
    self.canvas.pack()

    for y in range(CELL_COUNT):
      y_start = y * CELL_SIZE

      for x in range(CELL_COUNT):
        x_start = x * CELL_SIZE

        self.canvas.create_rectangle(
          x_start,
          y_start,
          x_start + CELL_SIZE,
          y_start + CELL_SIZE,
          fill="gray76"
        )

    boxes = [
      ((0,0), "red"),
      ((14,0), "cyan"),
      ((0,7), "green"),
      ((14,7), "magenta"),
      ((0,14), "blue"),
      ((7,7), "black"),
      ((14,14), "yellow"),
      ((7,0), "white"),
      ((7,14), "white")
    ]

    verticies = [
      (6,6), # inner
      (10,6),
      (6,10),
      (10,10),

      (5,5),
      (11,5),
      (5,11),
      (11,11),

      (4,4),
      (12,4),
      (4,12),
      (12,12),

      (3,3), # Outer
      (13,3),
      (3,13),
      (13,13),

      (3, 8), #left
      (4, 8),
      (5, 8),
      (6, 8),

      (10, 8), #right
      (11, 8),
      (12, 8),
      (13, 8),
    ]

    # draw boxes
    for box in boxes:
      coords, color = box
      start_x = coords[0] * CELL_SIZE
      start_y = coords[1] * CELL_SIZE
      self.canvas.create_rectangle(
          start_x,
          start_y,
          start_x + CELL_SIZE * 2,
          start_y + CELL_SIZE * 2,
          fill=color
        )

    for vert in verticies:
      (x, y) = vert
      offset = 6
      start_x = x * CELL_SIZE - offset
      start_y = y * CELL_SIZE - offset
      self.canvas.create_oval(
          start_x,
          start_y,
          start_x + offset * 2,
          start_y + offset * 2,
          fill="orange"
        )