import requests

def consulta_openstreetmap(logradouro, numero, bairro, cidade, estado):
    query = f'{logradouro} {numero} {bairro} {cidade} {estado}'
    url = f'https://nominatim.openstreetmap.org/search?format=json&limit=1&q={query}'
    try:
        resposta = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        dados = resposta.json()
        if dados:
            endereco = dados[0]
            return {
                'logradouro': endereco.get('address', {}).get('road', logradouro),
                'numero': numero,
                'bairro': endereco.get('address', {}).get('suburb', bairro),
                'cidade': endereco.get('address', {}).get('city', cidade),
                'estado': endereco.get('address', {}).get('state', estado),
                'cep': endereco.get('address', {}).get('postcode', None),
                'lat': endereco.get('lat', None),
                'lon': endereco.get('lon', None)
            }
        else:
            return None
    except:
        return None
