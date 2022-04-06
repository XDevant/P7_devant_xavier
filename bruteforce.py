from stocks import load_stocks
from models import Portfolio
from copy import deepcopy


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

fill_portfolios(brute_list, best_portfolio)

