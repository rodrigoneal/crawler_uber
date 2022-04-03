from dotenv import dotenv_values
from selenium_tools.selenium_driver import SeleniumDriver

from recibo_uber.pages.page import DadosViagem, Login
from recibo_uber.registro.registro import Registro
from recibo_uber.registro.to_csv import to_csv, from_csv

config = dotenv_values(".env")


driver = SeleniumDriver(log=False)
login = Login(driver, url='https://www.uber.com/br/pt-br/')
dados_viagem = DadosViagem(driver, 'https://riders.uber.com/trips')

login.open()
login.abrir_login.abrir_menu()
login.fazer_login.logar(usuario=config['username'], senha=config['password'])
dados_viagem.open()
dados = from_csv("dados_uber.csv")
dados = [Registro.from_dict(dado) for dado in dados]
dados = dados_viagem.pegar_dados.pegar_pagamento(dados)
to_csv(dados)
