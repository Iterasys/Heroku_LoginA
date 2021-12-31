#import os
import pytest
from pages import login_page

@pytest.fixture
def login(driver): # deixou de receber request e recebe diretamente driver
    return login_page.LoginPage(driver)  # instanciando a classe LoginPage e passando o Selenium

def testar_login_com_sucesso(login):
    # preencher o usuário, a senha e clicar no botão
    login.com_('tomsmith', 'SuperSecretPassword!')
    # validar a mensagem
    assert login.vejo_mensagem_de_sucesso()

def testar_login_com_usuario_invalido(login):
    # preencher o usuário, a senha e clicar no botão
    login.com_('asdfgasdfg', 'SuperSecretPassword!')
    # validar a mensagem
    assert login.vejo_mensagem_de_falha()

def testar_login_com_senha_invalida(login):
    # preencher o usuário, a senha e clicar no botão
    login.com_('tomsmith', 'xpto12345')
    # validar a mensagem
    assert login.vejo_mensagem_de_falha()
