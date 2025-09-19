import streamlit as st
from api_clients import consulta_openstreetmap
from utils import extrair_detalhes_endereco
from pdf_generator import gerar_pdf, gerar_mapa_statico

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
            st.write('Resultado do endereço:')
            st.json(resultado)

            mapa_img = gerar_mapa_statico(resultado['lat'], resultado['lon'])
            if mapa_img:
                st.image(mapa_img, caption='Mapa do local', use_column_width=True)

                if st.button('Gerar PDF com informações e mapa'):
                    pdf_bytes = gerar_pdf(resultado, mapa_img)
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
