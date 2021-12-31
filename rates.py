import abc


class CurrencyPair:

    @staticmethod
    def from_str(value: str, fallback_counter: str, seperator="/"):
        pairs = value.split(seperator)
        return CurrencyPair(base=pairs[0], counter=pairs[1] or fallback_counter)

    def __init__(self, base: str, counter: str):
        self.base = base.upper()
        self.counter = counter.upper()


class Ticker:

    def __init__(self, pair: CurrencyPair):
        self.pair = pair

    @abc.abstractmethod
    def query(self):
        raise NotImplementedError


class Rate:

    def __init__(self, pair: CurrencyPair, amount: float):
        self.pair = pair
        self.amount = amount

    def amount_formatted(self, precision=8):
        return "{:.{}f}".format(self.amount, precision).rstrip("0")
