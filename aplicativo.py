import streamlit as st
from api_clients import consulta_openstreetmap
from utils import extrair_detalhes_endereco
from pdf_generator import gerar_pdf
import requests

st.title('Consulta de Endereço com Mapa Interativo + Fotos Reais')

# Seu token Mapillary
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

            url_foto = buscar_foto_mapillary(MAPILLARY_TOKEN, float(resultado['lat']), float(resultado['lon']))

            if url_foto:
                st.image(url_foto, caption='Foto real da rua via Mapillary', use_column_width=True)
            else:
                st.warning('Nenhuma foto real próxima disponível no Mapillary para este endereço.')

            if st.button('Gerar PDF com informações'):
                pdf_bytes = gerar_pdf(resultado, None)
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
