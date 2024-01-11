from copy import copy
from .Cards import MainCards
from .SmallPlayer import SmallPlayer
import random
from .PokerOddsCalc.table import HoldemTable


class PokerGame:
    def __init__(self, players: list):
        self.isRunning = False
        self.playersInGame: list[SmallPlayer] = copy(players)
        self.allPlayers = copy(players)
        self.watchers: list[SmallPlayer] = []
        self.playerInMove = ""
        self.tokensOnTable = 0
        self.lastCall = 0
        self.round = 0
        self.cardsOnTable = []
        self.cards = []
        self.tableCards = []
        self.movesCounter = 0

    def nextPlayer(self):
        print("VERY IMPORTANT", self.playersInGame)
        for index, player in enumerate(self.playersInGame):
            print("HEEEEEEEEEEEERE", self.playerInMove)
            print(player.nick, index, (index + 1) % len(self.playersInGame) )
            if player.nick == self.playerInMove:

                self.playerInMove = self.playersInGame[(index + 1) % len(self.playersInGame)].nick
                break

    def getPlayersInGame(self):
        return len(self.playersInGame)

    def addWatcher(self, watcher):
        self.allPlayers.append(watcher)
        self.watchers.append(watcher)

    def newGame(self, players):
        self.playersInGame = players

    def mixCards(self):
        self.cards = random.sample(MainCards, len(MainCards))

    def nextTableCard(self):
        self.tableCards.append(self.cards.pop(0))

    def bet(self, move):
        self.lastCall = move.amount
        self.tokensOnTable += move.amount
        self.movesCounter += 1

    def call(self, move):
        self.tokensOnTable += self.lastCall
        self.movesCounter += 1
        if self.movesCounter >= len(self.playersInGame):
            self.round += 1
            self.movesCounter = 0
            return True
        return False

    def fold(self, move):
        for player in self.playersInGame:
            if player.nick == move.nick:
                self.playersInGame.remove(player)

    def startGame(self):
        self.playersInGame = copy(self.watchers)
        self.mixCards()
        for player in self.playersInGame:
            player.card1 = self.cards.pop(0)
            player.card2 = self.cards.pop(0)
        self.playerInMove = self.playersInGame[2%len(self.playersInGame)].nick
        self.isRunning = True
        return self.playersInGame[0], self.playersInGame[1]

    def getNextTableCard(self):
        if len(self.tableCards) < 5:
            self.cardsOnTable.append(self.cards.pop(0))
        return self.cardsOnTable

    def findWinner(self):
        table_cards = self.cardsOnTable
        winners = []
        max_score = 0

        for player in self.playersInGame:
            score = self.evaluate_hand(player, table_cards)
            if score > max_score:
                winners = [player.nick]
                max_score = score
            elif score == max_score:
                winners.append(player.nick)

        return winners

    def convert_cart_to_lib_poker(self, card):
        suit, rank = card.split('_')
        rank = rank[0].capitalize()
        if rank == '1':
            rank = 'T'
        suit_mapping = {'clubs': 'c', 'diamonds': 'd', 'hearts': 'h', 'spades': 's'}
        abbreviated_suit = suit_mapping.get(suit.lower(), suit.lower())
        return rank + abbreviated_suit

    def calculateBestHand(self):
        if len(self.cardsOnTable) == 5:
            for player in self.playersInGame:
                player.winPercentage = 0
                return
        holdem_game = self.create_holdem_calculator()
        a_dict = holdem_game.simulate()

        result_dict = {}

        for key, value in a_dict.items():
            if 'Win' in key:
                player_id = int(key.split()[1])
                result_dict[player_id] = value

        for id, player in enumerate(self.playersInGame):
            player.winPercentage = result_dict[id + 1]

    def create_holdem_calculator(self):
        holdem_game = HoldemTable(num_players=len(self.playersInGame), deck_type='full')
        for id, player in enumerate(self.playersInGame):
            holdem_game.add_to_hand(id + 1, [self.convert_cart_to_lib_poker(player.card1),
                                             self.convert_cart_to_lib_poker(player.card2)])
        new_list = []
        for card in self.cardsOnTable:
            new_list.append(self.convert_cart_to_lib_poker(card))
        holdem_game.add_to_community(new_list)
        return holdem_game

    def getWinner(self):
        holdem_game = self.create_holdem_calculator()
        winner_string = holdem_game.view_result()
        for i in range(1, len(self.playersInGame) + 1):
            if str(i) in winner_string:
                return self.playersInGame[i - 1].nick

    def resetGame(self):
        self.allPlayers = copy(self.watchers)
        self.playersInGame = copy(self.watchers)
        self.playerInMove = ""
        self.tokensOnTable = 0
        self.lastCall = 0
        self.round = 0
        self.cardsOnTable = []
        self.cards = []
        self.tableCards = []
        self.isRunning = False
        self.movesCounter = 0
