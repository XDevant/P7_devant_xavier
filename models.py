class Share:
    def __init__(self, id, df):
        self.id = id
        self.name = df["name"][id]
        self.price = df["price"][id]
        self.profit = df["profit"][id]
        self.income = round(self.price * self.profit / 100, 3)

    def __repr__(self):
        return f"{self.name}: {self.price}$, {self.profit}%, income {self.income}$"


class Portfolio:
    def __init__(self, shares):
        self.shares = shares
        self.cost = 0
        self.total_income = 0
        for share in shares:
            self.cost += share.price
            self.total_income += share.income

    def __repr__(self):
        itself = ""
        for share in self.shares:
            itself += share.__repr__() + "\n"
        return itself + f"Total:{self.cost}, Income:{self.total_income}"

    def buy(self, share):
        self.shares.append(share)
        self.cost += share.price
        self.total_income += share.income

    def sell(self, share):
        try:
            self.shares.remove(share)
            self.cost -= share.price
            self.total_income -= share.income
        except ValueError:
            pass