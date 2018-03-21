import tkinter as tk
from game_manager import *
from constants import *
import time

class GuiApplication(tk.Frame):
  def __init__(self, master=None, game_manager=None, robot=None):
    super().__init__(master)

    self.root = master
    self.game = game_manager
    self.robot = robot

    self.create_widgets()
    self.setup_canvas()
    self.update_canvas()
    self.pack()

    # Buttons
    self.master.bind('<KeyPress>', self.keydown)

    # Lift frame to top
    master.lift()
    master.call('wm', 'attributes', '.', '-topmost', True)
    master.after_idle(master.call, 'wm', 'attributes', '.', '-topmost', False)

  def keydown(self, e):
    x, y = self.robot.position
    speed = 5

    if e.keysym == 'Down':
      y += speed
    elif e.keysym == 'Up':
      y -= speed
    elif e.keysym == 'Left':
      x -= speed
    elif e.keysym == 'Right':
      x += speed

    # On top of empty coin
    elif e.keysym == '1':
      print('snapping to empty vertex')
      coin = self.game.get_closest_coin(x, y)
      coin.state = GameCoinState.NONEXISTANT
      self.canvas.itemconfig(
        self.canvas_entities['coins'][coin.id],
        fill='red'
      )
      x = coin.x
      y = coin.y

    # On top of active coin
    elif e.keysym == '2':
      print('snapping to new coin')
      coin = self.game.get_closest_coin(x, y)
      coin.state = GameCoinState.EXISTS
      self.canvas.itemconfig(
        self.canvas_entities['coins'][coin.id],
        fill='green'
      )
      x = coin.x
      y = coin.y

    self.robot.set_position(x, y)

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
    self.canvas = tk.Canvas(self, width=GRID_SIZE, height=GRID_SIZE)
    self.canvas.pack()
    self.canvas_entities = dict()

    for y in range(CELL_COUNT):
      y_start = y * CELL_SIZE

      for x in range(CELL_COUNT):
        x_start = x * CELL_SIZE

        self.canvas.create_rectangle(
          x_start,
          y_start,
          x_start + CELL_SIZE,
          y_start + CELL_SIZE,
          fill="gray76",  outline="gray60"
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

    # Draw path
    for p in self.game.temp_path:
      p1, p2 = p['points']
      coin_a = self.game.current_coins[str(p1)]
      coin_b = self.game.current_coins[str(p2)]

      self.canvas.create_line(
        coin_a.x, coin_a.y,
        coin_b.x, coin_b.y,
        fill="black", width=3
      )

    # Draw coins
    self.canvas_entities['coins'] = dict()
    for coin in self.game.current_coins.values():
      offset = 6
      start_x = coin.x - offset
      start_y = coin.y - offset

      # Draw
      self.canvas_entities['coins'][coin.id] = self.canvas.create_oval(
          start_x,
          start_y,
          start_x + offset * 2,
          start_y + offset * 2,
          fill='orange'
      )

      self.canvas.create_text(start_x, start_y, fill='white', text=coin.id)

    # Draw robot
    self.canvas_entities['robot'] = self.canvas.create_rectangle(
      self.robot.position[0],
      self.robot.position[1],
      self.robot.position[0] + 50,
      self.robot.position[1] + 50,
      fill="green"
    )

  def update_canvas(self):
    self.canvas.coords(
      self.canvas_entities['robot'],
      self.robot.position[0],
      self.robot.position[1],
      self.robot.position[0] + 50,
      self.robot.position[1] + 50,
    )
    self.canvas.update()
    
    self.root.after(100, self.update_canvas)