from copy import copy
from .Cards import MainCards
import random
class PokerGame:
    def __init__(self, players: list):
        self.playersInGame = copy(players),
        self.allPlayers = copy(players)
        self.watchers = []
        self.playerInMove = ""
        self.tokensOnTable = 0
        self.lastCall = 0
        self.round = 0
        self.cardsOnTable = []
        self.cards = []
        self.tableCards = []

    def getWinner(self):
        ...
    def nextPlayer(self):
        ...
    def nextRound(self):
        ...
    def getPlayersInGame(self):
        return len(self.playersInGame)
    def addWatcher(self, watcher):
        self.allPlayers.append(watcher)
        self.watchers.append(watcher)
    def newGame(self,players):
        self.playersInGame = players
    def mixCards(self):
        self.cards = random.sample(MainCards, len(MainCards))
    def nextTableCard(self):
        self.tableCards.append(self.cards.pop(0))
    def move(self,move):
        # coś
        self.nextPlayer()
