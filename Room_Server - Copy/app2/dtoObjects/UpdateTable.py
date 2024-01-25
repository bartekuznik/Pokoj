
class UpdateTable:
    def __init__(self, roomData, playersInGame):
        print(type(roomData), roomData)
        self.cardsOnTable = roomData["cardsOnTable"]
        self.nextPlayer = roomData["nextPlayer"]
        self.tokensOnTable = roomData["tokensOnTable"]
        self.lastCall = roomData["lastCall"]
        self.isFinished = roomData["isFinished"]
        self.playersInGame = playersInGame


    def to_json(self) -> dict:
        return {
            "type": "UpdateTable",
            "cardsOnTable": self.cardsOnTable,
            "nextPlayer": self.nextPlayer,
            "tokensOnTable": self.tokensOnTable,
            "lastCall": self.lastCall,
            "isFinished": self.isFinished,
            'playersInGame': self.playersInGame,
        }
