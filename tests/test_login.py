import unittest
from scrapper.scrapper import ScrapperINMET
import requests


class TestLogin(unittest.TestCase):

    def test_login_true(self):
        self.assertTrue(ScrapperINMET().login())

    def test_login_false(self):
        response = requests.get('http://www.inmet.gov.br/projetos/rede/pesquisa/inicio.php')
        self.assertFalse(ScrapperINMET().is_logged_in(response))