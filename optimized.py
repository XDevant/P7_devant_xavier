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
        self.df = pd.DataFrame([], columns=["name", "price", "profit", "income"])

    def __repr__(self):
        return self.df.__repr__()

    def buy(self, share, next_profit, index):
        share_df = pd.DataFrame([share], columns=["name", "price", "profit", "income"])
        self.df = pd.concat([self.df, share_df], axis=0, ignore_index=True)
        self.cash -= share["price"]
        self.total_income += share["income"]
        self.max_income = self.total_income + next_profit * self.cash / 100
        self.max_id = index

    def check_share(self, share):
        if share.price <= self.cash:
            return True
        return False

"""
    def sell(self, share):
        try:
            self.shares.remove(share)
            self.cost -= share.price
            self.total_income -= share.income
        except ValueError:
            pass
"""


def find_next_profit(index, df):
    """Used to return the profit of the share whose index is 1 more than the biggest index in portfolio
    and maximize the possible profit of a portofolio since df is sorted by desc. profit.
    """
    if index >= len(df) - 1:
        return 0
    else:
        return df["profit"][index + 1]


def build_first_best(df):
    """Bluntly builds a test portofofio by purchasing shares with best profit rate it can buy
    one after the other in a single itération.
    Used to quicly eliminate portofolios whit a maximum ideal estimated profit lesser than the current best candidate
    real profit"""
    first_best = Portfolio()
    for i in range(len(df)):
        share = df.loc[i]
        if first_best.check_share(share):
            first_best.buy(share, find_next_profit(i, df), i)
    return first_best


def create_first_candidates(best_portfolio, df):
    first_list = []
    for i in range(len(df)):
        share = df.loc[i]
        new = Portfolio()
        if new.check_share(share):
            next_profit = find_next_profit(i, df)
            new.buy(share, next_profit, i)
            if new.max_income > best_portfolio.total_income:
                first_list.append(new)
            else:
                break
    return first_list


def build_portfolios(portfolio, best_portfolio, df):
    new_list = []
    start_id = portfolio.max_id + 1
    for i in range(start_id, len(df)):
        new_portfolio = deepcopy(portfolio)
        next_profit = find_next_profit(i, df)
        share = df.loc[i]
        if new_portfolio.check_share(share):
            new_portfolio.buy(share, next_profit, i)
            if new_portfolio.max_income > best_portfolio.total_income:
                new_list.append(new_portfolio)
                if new_portfolio.total_income > best_portfolio.total_income:
                    best_portfolio = deepcopy(new_portfolio)
            else:
                break
    return new_list, best_portfolio


def fill_portfolios(list, best_portfolio, stock_df):
    next_list = []
    for portfolio in list:
        new_list, best_portfolio = build_portfolios(portfolio, best_portfolio, stock_df)
        if new_list != []:
            next_list += new_list
    if next_list == []:
        print(best_portfolio)
        print(f"Total income: {best_portfolio.total_income}")
    else:
        fill_portfolios(next_list, best_portfolio, stock_df)


def load_stocks(filemane):
    df = pd.read_csv(f"./{filemane}", delimiter=",")
    df = df[df["price"] > 0]
    df.drop_duplicates(inplace=True)
    df.dropna(inplace=True)
    return df


def chrono(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        func(*args, **kwargs)
        end = time.time()
        print(f"Time: {end - start}")
    return wrapper


@chrono
def main(argv):
    stock_df = load_stocks(argv[1])
    stock_df.sort_values("profit", ascending=False, inplace=True, kind="mergesort")
    stock_df.reset_index(inplace=True)
    stock_df["income"] = stock_df.apply(lambda row: row['price'] * row['profit'] / 100, axis=1)
    first_best = build_first_best(stock_df)
    new_list = create_first_candidates(first_best, stock_df)
    fill_portfolios(new_list, first_best, stock_df)


if __name__ == "__main__":
    main(sys.argv)


