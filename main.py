from dotenv import dotenv_values
from selenium_tools.selenium_driver import SeleniumDriver
from recibo_uber.pages.page import (DadosViagem, Login, DadosPagina)
from recibo_uber.registro.to_csv import to_csv

config = dotenv_values(".env")


driver = SeleniumDriver(log=False)
login = Login(driver, url='https://www.uber.com/br/pt-br/')
dados_viagem = DadosViagem(driver, 'https://riders.uber.com/trips')
dados_pagina = DadosPagina(driver)

login.open()
login.abrir_login.abrir_menu()
login.fazer_login.logar(usuario=config['username'], senha=config['password'])
dados_viagem.open()
paginas = dados_pagina.info_page.num_page()
# dados_viagem.pegar_dados.pegar_dados()
# dados = dados_viagem.pegar_dados.pegar_pagamento()
# to_csv(dados)
