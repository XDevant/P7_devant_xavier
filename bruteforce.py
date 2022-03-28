import pandas as pd


class Action:
    def __init__(self, id, df):
        self.id = id
        self.name = df["name"][id]
        self.price = df["price"][id]
        self.profit = df["profit"][id]


class Portfolio:
    def __init__(self, ids, df):
        self.ids = ids
        self.cost = 0
        self.gain = 0
        for id in ids:
            price = df["price"][id]
            self.cost += price
            self.gain += price * df["profit"][id] / 200

df = pd.read_csv("./datasettest_P7.csv", delimiter=",")
print(df["name"][0])
