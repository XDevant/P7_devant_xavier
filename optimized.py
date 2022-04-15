from copy import deepcopy
import pandas as pd
import sys
import time


class Portfolio:
    def __init__(self):
        self.cash = 500
        self.total_income = 0
        self.max_income = 0
        self.max_id = -1
        self.shares = []
        self.success = True

    def __repr__(self):
        return self.shares.__repr__()

    def buy(self, df, index):
        share = df.loc[index]
        if share.price <= self.cash:
            self.shares.append(index)
            self.cash -= share["price"]
            self.total_income += share["income"]
            self.max_income = self.estimate_max_income(df)
            self.success = True
        else:
            self.success = False
        self.max_id = index

    def sell_last(self, df):
        """Sells last bought share if exists but keeps it's index in max_id
        thus enabling backtracking"""
        if len(self.shares) > 0:
            share = df.loc[self.shares[-1]]
            self.shares = self.shares[:-1]
            self.cash += share["price"]
            self.total_income -= share["income"]
            self.max_income = self.estimate_max_income(df)
            return True
        return False

    def estimate_max_income(self, df):
        """Virtualy fills portfofio with remaining shares, including partialy
        buing of the first too expensive one.
        Used to compare with real income of the current best portfolio"""
        start_id = self.max_id + 1
        start = True
        max_income = self.total_income
        cash = self.cash
        for i in range(start_id, len(df)):
            share = df.loc[i]
            if start:
                if share.price <= cash:
                    start = False
                else:
                    continue
            if share.price <= cash:
                max_income += share["income"]
                cash -= share["price"]
            else:
                max_income += share["profit"] * cash / 100
                break
        return max_income


def build_first_best(df):
    """Builds a test portofofio by purchasing shares with best
    profit rate it can buy, one after the other in a single itération.
    Used to quicly eliminate portofolios with a maximum ideal
    estimated profit lesser than the current best candidate's real profit
    Also returns a list of partial portofolios every times we encounter
     a share too expensive to buy"""
    first_best = Portfolio()
    breaks = []
    breaking = False
    for i in range(len(df)):
        first_best.buy(df, i)
        if first_best.success:
            breaking = False
        else:
            if not breaking:
                breaks.append(deepcopy(first_best))
            breaking = True
    return first_best, breaks


def check_candidates(best_portfolio, breaks, df):
    for portfolio in breaks:
        portfolio.sell_last(df)
        start_id = portfolio.max_id + 1
        for i in range(start_id, len(df)):
            portfolio.buy(df, i)
            if portfolio.max_income <= best_portfolio.total_income:
                break
        if portfolio.total_income > best_portfolio.total_income:
            best_portfolio = deepcopy(portfolio)
    return best_portfolio


def load_stocks(filemane):
    """loads the df and drops corrupt rows"""
    df = pd.read_csv(f"./{filemane}", delimiter=",")
    df = df[df["price"] > 0]
    df.drop_duplicates(inplace=True)
    df.dropna(inplace=True)
    return df


def chrono(func):
    """Creates a wrapper to show calculation time"""
    def wrapper(*args, **kwargs):
        start = time.time()
        func(*args, **kwargs)
        end = time.time()
        print(f"Time: {round(end - start, 2)}")
    return wrapper


@chrono
def main(argv):
    df = load_stocks(argv[1])
    df.sort_values("profit", ascending=False, inplace=True, kind="mergesort")
    df.reset_index(inplace=True)
    df["income"] = df.apply(lambda r: r['price'] * r['profit'] / 100, axis=1)
    first_best, breaks = build_first_best(df)
    best_portfolio = check_candidates(first_best, breaks, df)
    for i in best_portfolio.shares:
        sh = df.loc[i]
        print(f"{sh.name}:    {sh.price}$  {sh.profit}%  {round(sh.income, 2)}$")
    print(f"Total income: {round(best_portfolio.total_income, 2)}$")
    print(f"Total Cost: {500 - round(best_portfolio.cash, 2)}$")


if __name__ == "__main__":
    main(sys.argv)
