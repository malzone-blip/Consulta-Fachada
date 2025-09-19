import streamlit as st
from api_clients import consulta_openstreetmap
from utils import extrair_detalhes_endereco
from pdf_generator import gerar_pdf

st.title('Consulta de Endereço com OpenStreetMap - Mapa Interativo')

endereco_texto = st.text_area(
    'Cole o endereço completo aqui (ex: Endereço: Rua X Número: 123 Bairro: Y Cidade: Z Estado: XX)',
    height=120
)

def gerar_iframe_osm(lat, lon, zoom=18, largura='100%', altura=400):
    bbox_padding = 0.001  # pequeno recuo para bbox
    left = float(lon) - bbox_padding
    right = float(lon) + bbox_padding
    top = float(lat) + bbox_padding
    bottom = float(lat) - bbox_padding

    iframe_html = f"""
    <iframe width="{largura}" height="{altura}" frameborder="0" scrolling="no"
    src="https://www.openstreetmap.org/export/embed.html?bbox={left},{bottom},{right},{top}&layer=mapnik&marker={lat},{lon}" 
    style="border:1px solid black"></iframe>
    """
    return iframe_html

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

            mapa_iframe = gerar_iframe_osm(resultado['lat'], resultado['lon'])
            st.markdown(mapa_iframe, unsafe_allow_html=True)

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
