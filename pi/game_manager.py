import json
from enum import Enum
from functools import reduce
from constants import *

class GameManager():
  def __init__(self, config_path):
    self.rounds = list()
    self.current_round_index = 0
    self.current_coins = dict()

    self._load_config(config_path)

  def get_current_round(self):
    return self.rounds[self.current_round_index]

  def next_round(self):
    self.current_round_index += 1
    if self.current_round_index >= len(self.rounds):
      self.current_round_index = 0
    
    self._setup_coins()

  def get_closest_coin(self, x, y):
    min_dist = float('inf')
    min_coin = None

    # Search for closest coin
    for coin in self.current_coins.values():
      d = (x - coin.x)**2 + (y - coin.y)**2
      if d < min_dist:
        min_dist = d
        min_coin = coin

    return min_coin

  def _setup_coins(self):
    self.current_coins = dict()

    for i in range(len(self.init_coins)):
      coin = self.init_coins[i]
      self.current_coins[i] = GameCoin(i, coin[0] * CELL_SIZE, coin[1] * CELL_SIZE)

  def _load_config(self, config_path):
    f = open(config_path, 'r')
    data = json.load(f)

    # Map out rounds
    for key in data['rounds'].keys():
      game_round = GameRound(key, data['rounds'][key])
      self.rounds.append(game_round)

    self.init_coins = data['coins']
    self._setup_coins()

class GameCoinState(Enum):
  UNVISITED = 1
  NONEXISTANT = 2
  EXISTS = 3
  DELIVERED = 4

class GameCoin():
  def __init__(self, id, x, y):
    self.state = GameCoinState.UNVISITED
    self.id = id
    self.x = x
    self.y = y

class GameRound():
  def __init__(self, title, coins):
    self.title = title
    self.coins = coins

  def get_total_coins(self):
    return reduce(lambda x, y: x + y, self.coins.values())

    

