import datetime

from requests_html import HTMLSession
from requests import Response
import re
import os
import configparser


class ScrapperINMET:

    def __init__(self):

        env_path = os.path.join(os.path.dirname(__file__), '..', 'env.ini')
        env_config = configparser.ConfigParser()
        env_config.read(env_path)
        self.user = env_config.get('login', 'user')
        self.password = env_config.get('login', 'password')

        self.base_url = "http://www.inmet.gov.br"
        self.session = HTMLSession(mock_browser=True)

    @staticmethod
    def is_logged_in(response: Response) -> bool:
        return 'Modulo de Estudo e Pesquisa' in response.text

    def login(self) -> bool:
        url = '/'.join([self.base_url, "projetos/rede/pesquisa/inicio.php"])
        self.session.get(url)

        payload = {
            'mUsuario': '',
            'mSenha': self.password,
            'mCod': self.user,
            'mGerModulo': 'PES',
            'btnProcesso': ' Acessar '
        }

        response = self.session.post(url, data=payload)
        response.raise_for_status()
        return self.is_logged_in(response)

    def get_dados_mes(self, uf: str, cidade: str, dtInicio: datetime.datetime, dtFim: datetime.datetime):

        self.login()

        url = '/'.join([self.base_url, "projetos/rede/pesquisa/form_mapas_mensal.php"])
        self.session.get(url)

        payload = {
            'mUsuario': self.user,
            'mRelRegiao': '',
            'mRelEstado': uf.upper(),
            'mRelDtInicio': dtInicio.strftime('%d/%m/%Y'),
            'mRelDtFim': dtFim.strftime('%d/%m/%Y'),
            'mGerModulo': 'PES',
            'mOpcaoAtrib15': '1',
            'btnProcesso': ' Pesquisa '
        }

        url = '/'.join([self.base_url, "projetos/rede/pesquisa/mapas_mensal_sem.php"])
        response = self.session.post(url, data=payload)
        pattern = cidade + '.*href=([^\>]+) target'
        url_result = re.search(pattern, response.text, flags=re.IGNORECASE).group(1)
        response = self.session.get(url_result)
        rtext = response.html.xpath('.//pre')[0].full_text
        dados = re.search('(estacao;.+)', rtext, re.IGNORECASE | re.DOTALL).group(1)

        dados = dados.split('\n')
        head = dados[0].split(';')
        dados.pop(0)
        result = list()
        for dado in dados:
            values = dado.split(';')
            if len(values) != len(head):
                continue
            temp = dict()
            for k, v in zip(head, values):
                if k + v == "":
                    continue
                temp[k] = v
            result.append(temp)
        return result
