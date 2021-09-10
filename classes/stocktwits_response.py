class StockTwitsResponse:
    def __init__(self, ticker, sentiment, message, randomization):
        self.ticker = ticker
        self.sentiment = sentiment
        self.message = message
        self.randomization = randomization

