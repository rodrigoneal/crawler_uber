import pandas as pd


def to_csv(dados):
    df = pd.DataFrame(dados)
    df.to_csv('dados_uber.csv', index=False, sep=';', encoding='1252')