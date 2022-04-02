from selenium_tools.page_objects import Page

from .elements import AbrirLogin, FazerLogin, PegarDados


class Login(Page):
    abrir_login = AbrirLogin()
    fazer_login = FazerLogin()


class DadosViagem(Page):
    pegar_dados = PegarDados()
