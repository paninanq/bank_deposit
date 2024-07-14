class NotSumm(Exception):
    def __init__(self):
        super().__init__("Summ should be more than 1000")


class NotDate(Exception):
    def __init__(self):
        super().__init__("The date entered does not exist")