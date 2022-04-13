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


    def buy(self, df, index):
        share = df.loc[index]
        if share.price <= self.cash:
            self.shares.append(index)
            self.cash -= share["price"]
            self.total_income += share["income"]
            self.max_id = index
            self.max_income = self.estimate_max_income(df)
        else:
            self.success = False


    def estimate_max_income(self, df):
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
    """Bluntly builds a test portofofio by purchasing shares with best profit rate it can buy
    one after the other in a single itération.
    Used to quicly eliminate portofolios with a maximum ideal estimated profit lesser than the current best candidate
    real profit"""
    first_best = Portfolio()
    for i in range(len(df)):
        first_best.buy(df, i)
    return first_best


def create_first_candidates(best_portfolio, df):
    first_list = []
    for i in range(len(df)):
        new = Portfolio()
        new.buy(df, i)
        if new.success and new.max_income > best_portfolio.total_income:
            first_list.append(new)
            if new.total_income > best_portfolio.total_income:
                best_portfolio = deepcopy(new)
        else:
            if new.success:
                break
    return first_list, best_portfolio


def build_portfolios(portfolio, best_portfolio, df):
    new_list = []
    start_id = portfolio.max_id + 1
    for i in range(start_id, len(df)):
        new_portfolio = deepcopy(portfolio)
        new_portfolio.buy(df, i)
        if new_portfolio.success and new_portfolio.max_income >= best_portfolio.total_income:
            new_list.append(new_portfolio)
            if new_portfolio.total_income > best_portfolio.total_income:
                best_portfolio = deepcopy(new_portfolio)
        else:
            if new_portfolio.success:
                break
    return new_list, best_portfolio


def fill_portfolios(list, best_portfolio, stock_df):
    next_list = []
    for portfolio in list:
        new_list, best_portfolio = build_portfolios(portfolio, best_portfolio, stock_df)
        if new_list != []:
            for portfolio in new_list:
                next_list.append(portfolio)
    if next_list == []:
        for i in best_portfolio.shares:
            share = stock_df.loc[i]
            print(f"{share['name']}    {share.price}  {share.profit}  {round(share.income, 2)}")
        print(f"Total income: {round(best_portfolio.total_income, 2)}")
        print(f"Total Cost: {round(500 - best_portfolio.cash, 2)}")
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
    new_list, first_best = create_first_candidates(first_best, stock_df)
    fill_portfolios(new_list, first_best, stock_df)


if __name__ == "__main__":
    main(sys.argv)


