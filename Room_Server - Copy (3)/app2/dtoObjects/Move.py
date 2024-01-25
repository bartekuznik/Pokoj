class Move:
    def __init__(self, nick, moveType, amount):
        self.nick = nick
        self.moveType = moveType
        self.amount = amount

    def to_json(self) -> dict:
        return {
            "type": "Move",
            "nick": self.nick,
            "moveType": self.moveType,
            "amount": self.amount
        }
