import re

def extrair_detalhes_endereco(texto):
    campos = {
        'logradouro': None,
        'numero': None,
        'bairro': None,
        'cidade': None,
        'estado': None
    }

    padroes = {
        'logradouro': r'End[e|ê]re[c|ç]o: ([^\n]+)',
        'numero': r'Número: ([^\n]+)',
        'bairro': r'Bairro: ([^\n]+)',
        'cidade': r'Cidade: ([^\n]+)',
        'estado': r'Estado: ([^\n]+)'
    }

    for chave, padrao in padroes.items():
        resultado = re.search(padrao, texto)
        if resultado:
            campos[chave] = resultado.group(1).strip()

    return campos

def cruzar_informacoes(dados_apis):
    chaves = ['logradouro', 'numero', 'bairro', 'cidade', 'estado', 'cep', 'lat', 'lon']
    resultado = {}
    for chave in chaves:
        valores = [d[chave] for d in dados_apis if d and d.get(chave)]
        if valores:
            resultado[chave] = max(set(valores), key=valores.count)
        else:
            resultado[chave] = None
    return resultado
