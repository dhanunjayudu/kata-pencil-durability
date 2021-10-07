from kata_pencil_durability import constants


class Paper:
    def __init__(self, data: str = ''):
        self.text = data
        self.last_erased = constants.last_erased
