import os
import pytest
from selenium import webdriver
from pages.login_page import LoginPage


@pytest.fixture
def login(request):
    # variavel local para armazenar o caminho do ChromeDriver
    print('>>> CWD == ' + os.getcwd())
    _chromedriver = 'vendor/chromedriver.exe'
    # _chromedriver = os.path.join(os.getcwd(), 'vendor', 'chromedriver.exe')

    if os.path.isfile(_chromedriver):
        # se existe um chromedriver dentro do projeto, instancie com ele
        driver_ = webdriver.Chrome(_chromedriver)  # ligando o Selenium
    else:
        # se não existe, tente usar um chromedriver publico no ambiente
        driver_ = webdriver.Chrome()
    loginPage = LoginPage(driver_)  # instanciando a classe LoginPage e passando o Selenium

    def quit():
        driver_.quit()  # desligar o Selenium

    # sinalizando o fim da execução para o ambiente
    request.addfinalizer(quit)
    return loginPage

    # Como eram os passos do jeito simples
    '''
    def old_login_valido(driver):
        driver.get('https://the-internet.herokuapp.com/login')
        driver.find_element(By.ID, 'username').send_keys('tomsmith')
        driver.find_element(By.ID, 'password').send_keys('SuperSecretPassword!')
        driver.find_element(By.CSS_SELECTOR, 'button.radius').click()
        assert driver.find_element(By.CSS_SELECTOR, 'div.flash.success').is_displayed()
    '''

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
