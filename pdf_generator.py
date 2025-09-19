from fpdf import FPDF
from io import BytesIO

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Relatório de Endereço', 0, 1, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(4)

    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, body)
        self.ln()

    def add_image(self, image_data, y_position=50):
        if image_data:
            self.add_page()
            imagem_stream = BytesIO(image_data)
            self.image(imagem_stream, x=10, y=y_position, w=190)

def gerar_pdf(dados, imagem_foto_bytes=None, imagem_mapa_bytes=None):
    pdf = PDF()
    pdf.add_page()

    texto = (f"Logradouro: {dados['logradouro']}\n"
             f"Número: {dados['numero']}\n"
             f"Bairro: {dados['bairro']}\n"
             f"Cidade: {dados['cidade']}\n"
             f"Estado: {dados['estado']}\n"
             f"CEP: {dados['cep'] if dados['cep'] else 'Não disponível'}")

    pdf.chapter_title('Informações do Endereço')
    pdf.chapter_body(texto)

    if imagem_mapa_bytes:
        pdf.chapter_title('Mapa Estático (OpenStreetMap)')
        pdf.add_image(imagem_mapa_bytes, y_position=50)

    if imagem_foto_bytes:
        pdf.chapter_title('Foto Real da Rua (Mapillary)')
        pdf.add_image(imagem_foto_bytes, y_position=50)

    pdf_bytes = pdf.output(dest='S').encode('latin1')
    return pdf_bytes
