from fpdf import FPDF
from io import BytesIO
from PIL import Image

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
        self.image(image_data, x=10, y=60, w=190)

def gerar_pdf(dados, imagem_bytes):
    pdf = PDF()
    pdf.add_page()
    texto = f"Logradouro: {dados['logradouro']}\nNumero: {dados['numero']}\nBairro: {dados['bairro']}\nCidade: {dados['cidade']}\nEstado: {dados['estado']}\nCEP: {dados['cep']}"
    pdf.chapter_title('Informações do Endereço')
    pdf.chapter_body(texto)

    temp_img = BytesIO(imagem_bytes)
    img = Image.open(temp_img)
    temp_img.seek(0)
    pdf.add_page()
    pdf.add_image(temp_img)

    pdf_output = BytesIO()
    pdf.output(pdf_output)
    pdf_output.seek(0)
    return pdf_output

def gerar_mapa_statico(lat, lon):
    GOOGLE_STATIC_MAPS_API_KEY = 'sua_chave_google_maps'
    url = f'https://maps.googleapis.com/maps/api/staticmap?center={lat},{lon}&zoom=18&size=600x400&markers=color:red%7C{lat},{lon}&key={GOOGLE_STATIC_MAPS_API_KEY}'
    try:
        resposta = requests.get(url)
        if resposta.status_code == 200:
            return resposta.content
        else:
            return None
    except:
        return None
