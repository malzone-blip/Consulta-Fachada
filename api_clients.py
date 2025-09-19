import requests

def consulta_openstreetmap(logradouro=None, numero=None, bairro=None, cidade=None, estado=None):
    base_url = "https://nominatim.openstreetmap.org/search"
    params = {
        'format': 'json',
        'addressdetails': 1,
        'limit': 1,
    }

    address_parts = []

    if logradouro:
        address_parts.append(logradouro)
    if numero:
        address_parts.append(numero)
    if bairro:
        address_parts.append(bairro)
    if cidade:
        address_parts.append(cidade)
    if estado:
        address_parts.append(estado)

    if not address_parts:
        return None

    params['q'] = ', '.join(address_parts)

    try:
        response = requests.get(base_url, params=params, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
        dados = response.json()
        if dados:
            resultado = dados[0]
            endereco = resultado.get('address', {})

            return {
                'logradouro': endereco.get('road') or endereco.get('pedestrian') or endereco.get('footway') or logradouro,
                'numero': endereco.get('house_number') or numero,
                'bairro': endereco.get('suburb') or bairro,
                'cidade': endereco.get('city') or endereco.get('town') or endereco.get('village') or cidade,
                'estado': endereco.get('state') or estado,
                'cep': endereco.get('postcode'),
                'lat': resultado.get('lat'),
                'lon': resultado.get('lon'),
            }
        else:
            return None

    except requests.RequestException:
        return None
