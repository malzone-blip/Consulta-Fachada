import streamlit as st
from api_clients import consulta_openstreetmap
from utils import extrair_detalhes_endereco
from pdf_generator import gerar_pdf
import requests

st.title('Consulta de Endereço com OpenStreetMap + Fotos Reais via Mapillary')

MAPILLARY_TOKEN = "MLY|24620608904235815|e6efa808100caa5ce0ed4751268cf95e"

endereco_completo = st.text_area(
    'Cole o endereço completo aqui (ex: Endereço: Rua X Número: 123 Bairro: Y Cidade: Z Estado: XX)',
    height=120
)

logradouro = st.text_input('Logradouro')
numero = st.text_input('Número')
bairro = st.text_input('Bairro')
cidade = st.text_input('Cidade')
estado = st.text_input('Estado')

def buscar_foto_mapillary(token, lat, lon):
    url = "https://graph.mapillary.com/images"
    params = {
        "access_token": token,
        "fields": "id,captured_at,thumb_2048_url",
        "closeto": f"{lon},{lat}",
        "limit": 1
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if 'data' in data and data['data']:
            return data['data'][0]['thumb_2048_url']
    return None

def get_osm_static_url(lat, lon, zoom=17, w=600, h=400):
    return f"https://staticmap.openstreetmap.de/staticmap.php?center={lat},{lon}&zoom={zoom}&size={w}x{h}&markers={lat},{lon},red-pushpin"

def montar_dados_pesquisa(campos):
    return {k: v for k, v in campos.items() if v.strip() != ''}

if st.button('Consultar'):
    campos_separados = {
        'logradouro': logradouro,
        'numero': numero,
        'bairro': bairro,
        'cidade': cidade,
        'estado': estado
    }

    if any(v.strip() != '' for v in campos_separados.values()):
        dados_extratos = montar_dados_pesquisa(campos_separados)
    else:
        dados_extratos = extrair_detalhes_endereco(endereco_completo)

    if dados_extratos:
        resultado = consulta_openstreetmap(**dados_extratos)

        if resultado and resultado['lat'] and resultado['lon']:
            st.subheader('Resultado do endereço:')
            st.markdown(f"""
            **Logradouro:** {resultado['logradouro']}  
            **Número:** {resultado['numero']}  
            **Bairro:** {resultado['bairro']}  
            **Cidade:** {resultado['cidade']}  
            **Estado:** {resultado['estado']}  
            **CEP:** {resultado['cep'] if resultado['cep'] else 'Não disponível'}  
            **Latitude:** {resultado['lat']}  
            **Longitude:** {resultado['lon']}  
            """)

            bbox_padding = 0.001
            left = float(resultado['lon']) - bbox_padding
            right = float(resultado['lon']) + bbox_padding
            top = float(resultado['lat']) + bbox_padding
            bottom = float(resultado['lat']) - bbox_padding

            mapa_iframe = f"""
                <iframe width="100%" height="400" frameborder="0" scrolling="no"
                src="https://www.openstreetmap.org/export/embed.html?bbox={left},{bottom},{right},{top}&layer=mapnik&marker={resultado['lat']},{resultado['lon']}" 
                style="border:1px solid black"></iframe>
                """
            st.markdown(mapa_iframe, unsafe_allow_html=True)

            url_mapa = get_osm_static_url(resultado['lat'], resultado['lon'])
            imagem_mapa = None
            try:
                resp_map = requests.get(url_mapa, timeout=8)
                resp_map.raise_for_status()
                imagem_mapa = resp_map.content
                st.image(imagem_mapa, caption='Mapa estático do local (OpenStreetMap)', use_column_width=True)
            except Exception:
                st.warning('Não foi possível baixar a imagem do mapa.')

            url_foto = buscar_foto_mapillary(MAPILLARY_TOKEN, float(resultado['lat']), float(resultado['lon']))
            imagem_foto = None
            if url_foto:
                try:
                    resposta_foto = requests.get(url_foto)
                    resposta_foto.raise_for_status()
                    imagem_foto = resposta_foto.content
                    st.image(imagem_foto, caption='Foto real da rua via Mapillary', use_column_width=True)
                except Exception:
                    st.warning('Não foi possível carregar a foto real da rua.')
            else:
                st.warning('Nenhuma foto real próxima disponível no Mapillary para este endereço.')

            pdf_bytes = gerar_pdf(resultado, imagem_foto, imagem_mapa)

            if pdf_bytes:
                st.download_button(
                    label='Download do PDF com mapa e foto da rua',
                    data=pdf_bytes,
                    file_name='endereco_consulta.pdf',
                    mime='application/pdf'
                )
        else:
            st.error('Não foi possível localizar o endereço na API OpenStreetMap.')
    else:
        st.error('Não foi possível extrair dados válidos para consulta.')
