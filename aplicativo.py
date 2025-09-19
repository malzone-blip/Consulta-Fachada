import streamlit as st
from api_clients import consulta_openstreetmap
from utils import extrair_detalhes_endereco, url_mapa_estatico_osm
from pdf_generator import gerar_pdf
import requests

st.title('Consulta de Endereço com OpenStreetMap + Fotos Reais via Mapillary')

MAPILLARY_TOKEN = "MLY|24620608904235815|e6efa808100caa5ce0ed4751268cf95e"

endereco_texto = st.text_area(
    'Cole o endereço completo aqui (ex: Endereço: Rua X Número: 123 Bairro: Y Cidade: Z Estado: XX)',
    height=120
)

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

if st.button('Consultar'):
    dados_extratos = extrair_detalhes_endereco(endereco_texto)
    if all(dados_extratos.values()):
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

            # Baixar e mostrar mapa estático
            url_mapa = url_mapa_estatico_osm(resultado['lat'], resultado['lon'])
            imagem_mapa = None
            try:
                resposta_mapa = requests.get(url_mapa, timeout=5)
                resposta_mapa.raise_for_status()
                imagem_mapa = resposta_mapa.content
                st.image(imagem_mapa, caption='Mapa estático do local (OpenStreetMap)', use_column_width=True)
            except Exception:
                st.error('Não foi possível carregar a imagem do mapa devido a restrições de rede.')

            # Buscar e mostrar foto real no Mapillary
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

            if st.button('Gerar PDF com informações e imagens'):
                pdf_bytes = gerar_pdf(resultado, imagem_mapa, imagem_foto)
                st.download_button(
                    label='Download do PDF',
                    data=pdf_bytes,
                    file_name='endereco_consulta.pdf',
                    mime='application/pdf'
                )
        else:
            st.error('Não foi possível localizar o endereço na API OpenStreetMap.')
    else:
        st.error('Por favor, preencha todas as informações no campo de endereço.')
