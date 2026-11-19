import pandas as pd
import numpy as np

COLS = ['unit', 'cycle', 'op1', 'op2', 'op3'] + [f'sensor_{i}' for i in range(1, 22)]

def load_set(train_path, test_path, rul_path):
    train = pd.read_csv(train_path, sep=r'\s+', header=None, names=COLS)
    test = pd.read_csv(test_path, sep=r'\s+', header=None, names=COLS)
    rul_test = pd.read_csv(rul_path, sep=r'\s+', header=None, names=['RUL'])
    return train, test, rul_test

def add_rul_train(train):
    max_cycle = train.groupby('unit')['cycle'].max().reset_index()
    max_cycle.columns = ['unit', 'max_cycle']
    train = train.merge(max_cycle, on='unit')
    train['RUL'] = train['max_cycle'] - train['cycle']
    train.drop('max_cycle', axis=1, inplace=True)
    return train

def add_rul_test(test, rul_test):
    max_cycle = test.groupby('unit')['cycle'].max().reset_index()
    max_cycle.columns = ['unit', 'max_cycle']
    rul_test = rul_test.reset_index().rename(columns={'index': 'unit_idx'})
    rul_test['unit'] = rul_test['unit_idx'] + 1
    max_cycle = max_cycle.merge(rul_test[['unit', 'RUL']], on='unit')
    test = test.merge(max_cycle, on='unit')
    test['RUL'] = test['max_cycle'] - test['cycle'] + test['RUL']
    test.drop('max_cycle', axis=1, inplace=True)
    return test

if __name__ == "__main__":
    train, test, rul_test = load_set('data/train_FD001.txt', 'data/test_FD001.txt', 'data/RUL_FD001.txt')
    print("Train shape:", train.shape, "| Units:", train['unit'].nunique())
    print("Test shape:", test.shape, "| Units:", test['unit'].nunique())
    train = add_rul_train(train)
    test = add_rul_test(test, rul_test)
    print(train[['unit', 'cycle', 'RUL']].head())
    print("Max cycles per engine (train) - min/max/mean:",
          train.groupby('unit')['cycle'].max().min(),
          train.groupby('unit')['cycle'].max().max(),
          round(train.groupby('unit')['cycle'].max().mean(), 1))
    train.to_parquet('data/train_FD001_rul.parquet')
    test.to_parquet('data/test_FD001_rul.parquet')
