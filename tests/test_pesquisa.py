from datetime import datetime
import unittest
from scrapper.scrapper import ScrapperINMET


class TestPesquisa(unittest.TestCase):

    def test_pesquisa_mes(self):
        scrap = ScrapperINMET()
        result = scrap.get_dados_mes('ba', 'salvador', datetime(2016, 1, 1), datetime(2017, 1, 1))
        self.assertEqual(len(result), 12)
