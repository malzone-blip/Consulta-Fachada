import streamlit as st
from api_clients import consulta_openstreetmap
from utils import extrair_detalhes_endereco, url_mapa_estatico_osm
from pdf_generator import gerar_pdf
import requests

st.title('Consulta de Endereço com OpenStreetMap')

endereco_texto = st.text_area(
    'Cole o endereço completo aqui (ex: Endereço: Rua X Número: 123 Bairro: Y Cidade: Z Estado: XX)',
    height=120
)

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

            url_mapa = url_mapa_estatico_osm(resultado['lat'], resultado['lon'])
            resposta_mapa = requests.get(url_mapa)
            if resposta_mapa.status_code == 200:
                st.image(resposta_mapa.content, caption='Mapa do local', use_column_width=True)

                if st.button('Gerar PDF com informações e mapa'):
                    pdf_bytes = gerar_pdf(resultado, resposta_mapa.content)
                    st.download_button(
                        label='Download do PDF',
                        data=pdf_bytes,
                        file_name='endereco_consulta.pdf',
                        mime='application/pdf'
                    )
            else:
                st.error('Não foi possível carregar a imagem do mapa.')
        else:
            st.error('Não foi possível localizar o endereço na API OpenStreetMap.')
    else:
        st.error('Por favor, preencha todas as informações no campo de endereço.')
