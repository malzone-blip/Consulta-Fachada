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

    def add_image(self, image_data):
        # Adiciona imagem se image_data não for None
        if image_data:
            self.add_page()
            # image_data deve ser um BytesIO ou caminho para arquivo
            self.image(image_data, x=10, y=60, w=190)

def gerar_pdf(dados, imagem_bytes=None):
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

    if imagem_bytes:
        from io import BytesIO
        imagem_stream = BytesIO(imagem_bytes)
        pdf.add_image(imagem_stream)

    pdf_output = BytesIO()
    pdf.output(pdf_output)
    pdf_output.seek(0)
    return pdf_output
