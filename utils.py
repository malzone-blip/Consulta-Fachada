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

def url_mapa_estatico_osm(lat, lon, zoom=18, largura=600, altura=400):
    return f'https://staticmap.openstreetmap.de/staticmap.php?center={lat},{lon}&zoom={zoom}&size={largura}x{altura}&markers={lat},{lon},red'
