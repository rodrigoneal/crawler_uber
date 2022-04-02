from time import sleep

from selenium.common.exceptions import (ElementClickInterceptedException,
                                        NoSuchElementException,
                                        StaleElementReferenceException,
                                        TimeoutException)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium_tools.page_objects import Element

from recibo_uber.registro.registro import Registro


def gerar_link():
    cont = 10
    while True:
        link = 'https://riders.uber.com/trips?offset={}&fromTime&toTime'
        _temp = link.format(cont)
        yield _temp
        cont += 10

class AbrirLogin(Element):
    abrir_submenu = (
        By.XPATH, "/html/body/div[1]/div/div/div[1]/main/nav/div/ul[4]/li[4]/button")
    faca_login = (
        By.XPATH, "/html/body/div[1]/div/div/div[2]/div/div/div/div[2]/div/div[4]/section/div/div/div/div/div[3]/a/div[2]/h2")

    def abrir_menu(self):
        self.find_element(self.abrir_submenu).click()
        sleep(2)
        self.find_element(self.faca_login).click()


class FazerLogin(Element):
    username = (By.ID, "mobile")
    password = (By.ID, "password")
    mensagem = (By.ID, "smsOTP")
    btn_avancar = (By.ID, "next-button")
    erro_tentativas = (By.ID, "error-caption-mobile")
    rede_social = (By.TAG_NAME, 'a')
    facebook = (
        By.XPATH, '/html/body/div[1]/div/div/div/div/div/a[1]/div/div[2]')
    user_face = (By.ID, 'email')
    pass_face = (By.ID, 'pass')
    btn_face = (By.ID, "loginbutton")

    def login_rede_social(self, usuario, senha):
        self.find_element(self.rede_social).click()
        sleep(1)
        self.find_element(self.facebook).click()
        sleep(1)
        self.find_element(self.user_face).send_keys(usuario)
        sleep(1)
        self.find_element(self.pass_face).send_keys(senha)
        sleep(1)
        self.find_element(self.btn_face).click()

    def logar(self, usuario, senha):
        self.login_rede_social(usuario, senha)


class PegarDados(Element):
    cards = (By.XPATH, '//div[2]/div/div[2]/div/div[1]/div/div/div[2]/div')
    plus = (By.TAG_NAME, 'svg')
    paginate = (
        By.XPATH, '/html/body/div[1]/div[1]/div/div[2]/div/div[2]/div/div[1]/div/div/div[3]/div[2]')
    divs = (By.CLASS_NAME, 'ag')
    dados = []
    current_url = None
    count = 0
    link = (By.PARTIAL_LINK_TEXT, 'Informações')
    recibo = (
        By.XPATH, '//div/div[2]/div/div/div/div/div[1]/div[2]/div[2]/div[2]')
    pagamento = (
        By.XPATH, '//table[6]/tbody/tr/td/table[2]/tbody/tr/td[1]/table/tbody/tr/td/table[2]/tbody/tr[1]/td')
    frame_baner = (By.ID, 'unified-receipt-iframe')
    alt_pagamento = (By.XPATH, '//td/table[5]/tbody/tr/td/table[3]/tbody/tr/td[1]/table/tbody/tr/td/table[2]/tbody/tr/td')
    alt_pagamento_2 = (By.XPATH, '//td/table[4]/tbody/tr/td/table[3]/tbody/tr/td[1]/table/tbody/tr/td/table[2]/tbody/tr/td')
    gerador_url = gerar_link()

       

    def get_cards(self):
        tentativa = 0
        while True:
            try:
                cards = self.find_elements(self.cards)
                cards[0].find_element(*self.plus)
                return cards
            except:
                tentativa += 1
                if tentativa > 5:
                    self.driver.refresh()
                    sleep(3)
                elif tentativa > 10:
                    raise TypeError
                pass

    def _open_card(self, card):
        tentativa = 0
        espera = 0
        if card.get_attribute('data-trip-expanded') == 'false':
            try:
                card.find_element(*self.plus).click()
                while card.get_attribute('data-trip-expanded') == 'false':
                    sleep(0.1)
                    espera += 1
                    if espera % 5 == 0:
                        card.find_element(*self.plus).click()
            except:
                tentativa += 1
                if tentativa > 10:
                    raise TypeError
                pass
    def pegar_dados(self):
        self.current_url = self.driver.current_url
        while True:
            cards = self.get_cards()
            for card in cards:
                registro = Registro()
                self._open_card(card)
                try:
                    dados = card.find_elements(*self.divs)
                except:
                    continue
                try:
                    link = card.find_element(*self.link).get_attribute('href')
                except NoSuchElementException:
                    sleep(0.2)
                    link = card.find_element(*self.link).get_attribute('href')
                _temp = []
                for dado in dados:
                    _temp.append(dado.text)
                _reg = registro.save_registro(_temp, link)
                self.dados.append(_reg)
            paginate = self.find_element(self.paginate)
            if paginate.get_attribute('disabled') == 'true':
                return self.dados
            else:
                _link_url = next(self.gerador_url)
                self.driver.get(_link_url)


    def limpar_pagamento(self, pagamento: str):
        sujeiras = ('Mastercard ••••', 'Visa ••••', 'Mastercard Crédito ••••', 'Mastercard Débito ••••')
        if pagamento:
            for sujeira in sujeiras:
                pagamento = pagamento.replace(sujeira, '')
            return pagamento

    def _pagamento(self):
        for element in (self.pagamento, self.alt_pagamento, self.alt_pagamento_2):
            try:
                pagamento = self.find_element(element, time=1).text
                return pagamento
            except:
                pass
        raise TypeError()


    def pegar_pagamento(self):
        for dado in self.dados:           
            if not dado.pagamento:
                self.driver.get(dado.link)
                try:
                    recibo = self.find_element(self.recibo)
                    if recibo.text.strip().lower() == 'Ver recibo'.lower():
                        recibo.click()
                    else:
                        print(recibo.text)
                        continue
                except:
                    sleep(0.5)
                    try:
                        recibo = self.find_element(self.recibo)
                    except:
                        continue
                    if recibo.text.strip().lower() == 'Ver recibo'.lower():
                        recibo.click()
                    else:
                        print(recibo.text)
                        continue
                for _ in range(20):
                    self.driver.switch_to.default_content()
                    try:
                        frame = self.find_element(self.frame_baner, time=2)
                        break
                    except:
                        try:
                            self.find_element(self.recibo, time=1).click()
                        except:
                            pass
                        pass              
                sleep(0.5)                
                self.change_frame(frame)
                for _ in range(10):
                    try:
                        pagamento = self._pagamento()
                    except:
                        self.driver.switch_to.default_content()
                        frame = self.find_element(self.frame_baner, time=2)
                        self.change_frame(frame)
                if not pagamento:
                    pagamento = None
                else: 
                    pagamento = self.limpar_pagamento(pagamento)           
                dado.pagamento = pagamento
        return self.dados
