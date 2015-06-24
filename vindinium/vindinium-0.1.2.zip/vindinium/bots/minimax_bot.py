import random
import vindinium as vin
from vindinium.bots import BaseBot
from vindinium.ai import Minimax

__all__ = ['MinimaxBot']

class MinimaxBot(BaseBot):
    '''Minimax bot.'''
    
    search = None

    def __init__(self, max_depth=8):
        super(MinimaxBot, self).__init__()
        self.max_depth = max_depth

    def start(self):
        self.search = Minimax(self.game, self.max_depth)

    def move(self):
        moves = self.search.find()
        return moves[0]