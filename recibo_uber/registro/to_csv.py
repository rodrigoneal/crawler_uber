import pandas as pd
from recibo_uber.registro.registro import Registro


def to_csv(dados):
    df = pd.DataFrame(dados)
    df.to_csv('dados_uber.csv', index=False, sep=';', encoding='1252')

def from_csv(path):
    df = pd.read_csv(path, sep=";", encoding="1252")
    return df[df['pagamento'].isna()].to_dict(orient="records")

