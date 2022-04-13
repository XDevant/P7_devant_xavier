from copy import deepcopy
import pandas as pd


class Share:
    def __init__(self, id, df):
        self.id = id
        self.name = df["name"][id]
        self.price = df["price"][id]
        self.profit = df["profit"][id]
        self.income = round(self.price * self.profit / 100, 3)

    def __repr__(self):
        return f"{self.name}: {self.price}$, {self.profit}%, income {round(self.income, 2)}$"


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
        return itself + f"Cost:{self.cost}, Income:{round(self.total_income, 2)}"

    def buy(self, share):
        self.shares.append(share)
        self.cost += share.price
        self.total_income += share.income


def load_stocks(index):
    df = pd.read_csv(f"./dataset{index}_Python+P7.csv", delimiter=",")
    stocks = [Share(i, df) for i in range(len(df))]
    return stocks


def build_portfolio(portfolio, best_portfolio):
    new_list = []
    start_id = portfolio.shares[-1].id + 1
    for i in range(start_id, total):
        new_portfolio = deepcopy(portfolio)
        new_portfolio.buy(stock_list[i])
        if new_portfolio.cost <= 500:
            new_list.append(new_portfolio)
            if new_portfolio.total_income > best_portfolio.total_income:
                best_portfolio = deepcopy(new_portfolio)
    return new_list, best_portfolio


def fill_portfolios(list, best_portfolio):
    next_list = []
    for portfolio in list:
        new_list, best_portfolio = build_portfolio(portfolio, best_portfolio)
        if new_list != []:
            next_list += new_list
    if next_list == []:
        print(best_portfolio)
    else:
        fill_portfolios(next_list, best_portfolio)


stock_list = load_stocks(0)
total = len(stock_list)
best_portfolio = Portfolio([])
brute_list = []

for stock in stock_list:
    new = Portfolio([])
    new.buy(stock)
    if new.cost <= 500:
        brute_list.append(new)
        if new.total_income > best_portfolio.total_income:
            best_portfolio = deepcopy(new)
fill_portfolios(brute_list, best_portfolio)

