# 1 - Bibliotecas
from selenium.webdriver.common.by import By
from pages.base_page import BasePage # receber as funções da base_page

# 2 - Classe
class LoginPage(BasePage):
    # 2.1 - Mapeamento dos Elementos da Página
    _username_input = {'by': By.ID, 'value': 'username'}
    _password_input = {'by': By.ID, 'value': 'password'}
    _login_button = {'by': By.CSS_SELECTOR, 'value': 'button.radius'}
    _success_message = {'by': By.CSS_SELECTOR, 'value': 'div.flash.success'}
    _failure_message = {'by': By.CSS_SELECTOR, 'value': 'div.flash.error'}
    _login_form = { 'by': By.ID, 'value': 'login'}

    # Erro: Descoberto pelo proprio autor
    # Defeito: Descoberto de forma estática por outra pessoa
    # Falha: Descoberto de forma dinâmica por outra pessoa

    # 2.2 - Inicializador / Construtor (Java)
    def __init__(self, driver):
        # instanciando o Selenium
        self.driver = driver
        # abrindo a página alvo
        self._entrar('/login')
        # validando se o formulário de login está visível
        assert self._aparecer(self._login_form)

    def com_(self, username, password):
        '''
        # Programação Comum - Sem Page Object
        self.driver.find_element(self._username_input['by'],
                                 self._username_input['value']).send_keys(username)
        self.driver.find_element(self._password_input['by'],
                                 self._password_input['value']).send_keys(password)
        self.driver.find_element(self._login_button['by'],
                                 self._login_button['value']).click()
        '''

        self._escrever(self._username_input, username)
        self._escrever(self._password_input, password)
        self._clicar(self._login_button)

    # 2.3 - Ações Realizaveis
    def vejo_mensagem_de_sucesso(self):
        '''
        return self.driver.find_element(self._success_message['by'],
                                        self._success_message['value']).is_displayed()
        '''
        return self._aparecer(self._success_message, 10)

    def vejo_mensagem_de_falha(self):
        '''
        return self.driver.find_element(self._failure_message['by'],
                                        self._failure_message['value']).is_displayed()
        '''
        return  self._aparecer(self._failure_message, 10)

    def testar_login_com_sucesso(self, login):
        # preencher o usuário, a senha e clicar no botão
        login.com_('tomsmith', 'SuperSecretPassword!')
        # validar a mensagem
        assert login.vejo_mensagem_de_sucesso()

    def testar_login_com_usuario_invalido(self, login):
        # preencher o usuário, a senha e clicar no botão
        login.com_('asdfgasdfg', 'SuperSecretPassword!')
        # validar a mensagem
        assert login.vejo_mensagem_de_falha()

    def testar_login_com_senha_invalida(self, login):
        # preencher o usuário, a senha e clicar no botão
        login.com_('tomsmith', 'xpto12345')
        # validar a mensagem
        assert login.vejo_mensagem_de_falha()
