import re


class ExtratorURL:
    def __init__(self, url):
        """Salva a url em um atributo do objeto (self.url = url) e verifica se a url é válida."""
        self.url = self.sanitiza_url(url)
        self.valida_url()

    def sanitiza_url(self, url):
        """Retorna a url removendo espaços em branco."""
        if type(url) == str:
            return url.strip()
        else:
            return ""

    def valida_url(self):
        """Valida se a url está vazia."""
        padrao_url = re.compile('(http(s)?://)?(www.)?bytebank.com(.br)?/cambio')
        match = padrao_url.match(self.url)

        if not match:
            raise ValueError("A URL não é válida.")

    def get_url_base(self):
        """Retorna a base da url."""
        indice_interrogacao = self.url.find('?')
        url_base = self.url[:indice_interrogacao]
        return url_base

    def get_url_parametros(self):
        """Retorna os parâmetros da url."""
        indice_interrogacao = self.url.find('?')
        url_parametros = self.url[indice_interrogacao + 1:]
        return url_parametros

    def get_valor_parametro(self, parametro_busca):
        """Retorna o valor do parâmetro `parametro_busca`."""
        indice_parametro = self.get_url_parametros().find(parametro_busca)
        tamanho_parametro = len(parametro_busca)
        indice_valor = indice_parametro + tamanho_parametro + 1
        indice_e_comercial = self.get_url_parametros().find('&', indice_valor)

        if indice_e_comercial == -1:
            valor = self.get_url_parametros()[indice_valor:]
        else:
            valor = self.get_url_parametros()[indice_valor:indice_e_comercial]

        return valor

    def __len__(self):
        return len(self.url)

    def __str__(self):
        return self.url + "\n" + "Parâmetros: " + self.get_url_parametros() + "\n" + "URL Base: " + self.get_url_base()

    def __eq__(self, other):
        return self.url == other.url
    
    def converter_destino(self):
        _dolar = 5.50
        _moeda_origem = self.get_valor_parametro('moedaOrigem')
        _moeda_destino = self.get_valor_parametro('moedaDestino')
        _quantidade = float(self.get_valor_parametro('quantidade'))
        if _moeda_destino == 'dolar':
            _quantidade_convertida = _quantidade * _dolar
            return f'${float(_quantidade_convertida)}'
        else:
            raise ValueError('Moeda de destino não contida no banco de dados.')



extrator_url = ExtratorURL("bytebank.com/cambio?moedaDestino=dolar&quantidade=100&moedaOrigem=real")
valor_quantidade = extrator_url.get_valor_parametro("quantidade")
conversao = extrator_url.converter_destino()
print(valor_quantidade)
print(conversao)
