import pandas as pd
from models import Share

df = pd.read_csv("./dataset0_Python+P7.csv", delimiter=",")

def load_stocks(index):
    df = pd.read_csv(f"./dataset{index}_Python+P7.csv", delimiter=",")
    stocks = [Share(i, df) for i in range(len(df))]
    return stocks
