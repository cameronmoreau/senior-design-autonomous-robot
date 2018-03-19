import json
from functools import reduce

class GameManager():
  def __init__(self, config_path):
    self.rounds = []
    self.current_round_index = 0

    self._load_config(config_path)

  def get_current_round(self):
    return self.rounds[self.current_round_index]

  def next_round(self):
    self.current_round_index += 1
    if self.current_round_index >= len(self.rounds):
      self.current_round_index = 0

  def _load_config(self, config_path):
    f = open(config_path, 'r')
    data = json.load(f)

    # Map out rounds
    for key in data['rounds'].keys():
      game_round = GameRound(key, data['rounds'][key])
      self.rounds.append(game_round)

    self.init_coins = data['coins']

class GameRound():
  def __init__(self, title, coins):
    self.title = title
    self.coins = coins

  def get_total_coins(self):
    return reduce(lambda x, y: x + y, self.coins.values())

    

