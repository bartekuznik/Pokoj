class Greeting:

    def __init__(self, hello):
        self.hello = hello

    def to_json(self) -> dict:
        return {
            "type": "Greeting",
            "hello": self.hello
        }
