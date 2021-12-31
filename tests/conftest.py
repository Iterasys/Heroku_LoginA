import os

import pytest
from selenium import webdriver
from selenium.webdriver import firefox

from . import config

def pytest_addoption(parser):
    parser.addoption(
        '--baseurl',
        action='store',
        default='https://the-internet.herokuapp.com',
        help='Url base da aplicacao alvo do teste'
    )
    parser.addoption(
        '--host',
        action='store',
        default='saucelabs',
        help='Onde vamos executar nossos testes: localhost ou saucelabs'
    )
    parser.addoption(
        '--browser',
        action='store',
        default='chrome',
        help='O nome do navegador utilizado nos testes'
    )
    parser.addoption(
        '--browserversion',
        action='store',
        default='96.0',
        help='Versão do browser'
    )
    parser.addoption(
        '--platform',
        action='store',
        default='Windows 10',
        help='Sistema Operacional a ser utilizado durante os testes (apenas no saucelabs)'
    )

@pytest.fixture
def driver(request): # Inicialização dos testes - similar a um Before / Setup
    config.baseurl = request.config.getoption('--baseurl')
    config.host = request.config.getoption('--host')
    config.browser = request.config.getoption('--browser')
    config.browserversion = request.config.getoption('--browserversion')
    config.platform = request.config.getoption('--platform')

    if config.host == 'saucelabs':
        test_name = request.node.name #nome do teste
        capabilities = {
            'browserName': config.browser,
            'browserVersion': config.browserversion,
            'platformName': config.platform,
            'sauce:options': {
                'name': test_name
            }
        }
        #_credentials = os.environ['InstrutorIterasys06'] + ':' + os.environ['1ac20078-c9c4-44ce-afe5-a153f7c83aa2']
        #_url = 'https://' + _credentials + '@ondemand.us-west-1.saucelabs.com:443/wd/hub'
        _url = 'https://InstrutorIterasys06:1ac20078-c9c4-44ce-afe5-a153f7c83aa2@ondemand.us-west-1.saucelabs.com:443/wd/hub'
        driver_ = webdriver.Remote(_url, capabilities)
    else: # execução local / localhost
        if config.browser == 'chrome':
            _chromedriver = os.path.join(os.getcwd(), 'vendor', 'chromedriver.exe')
            if os.path.isfile(_chromedriver):
                driver_ = webdriver.Chrome(_chromedriver)
            else:
                driver_ = webdriver.Chrome()
        elif config.browser == 'firefox':
            _geckodriver = os.path.join(os.getcwd(), 'vendor', 'geckodriver.exe')
            if os.path.isfile(_geckodriver):
                driver_ = webdriver.Firefox(_geckodriver)
            else:
                driver_ = webdriver.Firefox()

    def quit(): # Finalização dos testes - similar ao After ou TearDown
        # sinalização de passou ou falhou conforme o retorno da requisição
        sauce_result = 'failed' if request.node.rep_call.failed else 'passed'
        driver_.execute_script('sauce:job-result={}'.format(sauce_result))
        driver_.quit()

    request.addfinalizer(quit)
    return driver_

@pytest.hookimpl(hookwrapper=True, tryfirst=True) # Implementação do gatilho de comunicação com SL
def pytest_runtest_makereport(item, call):
    # parametros para geração do relatório / informações dos resultados
    outcome = yield
    rep = outcome.get_result()

    # definir atributos para o relatório
    setattr(item, 'rep_' + rep.when, rep)