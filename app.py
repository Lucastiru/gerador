# Requisitos: Flask, WeasyPrint
# Instale com: pip install flask weasyprint

from flask import Flask, render_template_string, request, send_file
from weasyprint import HTML
import tempfile
import os

app = Flask(__name__)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="pt">
<head>
    <meta charset="UTF-8">
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f4f4f4;
            padding: 2cm;
        }
        .etiqueta {
            width: 18cm;
            border: 2px solid #333;
            padding: 1.5cm;
            background-color: #ffffff;
            border-radius: 10px;
            margin-bottom: 2cm;
        }
        .titulo {
            font-size: 22px;
            font-weight: bold;
            margin-bottom: 0.5cm;
            border-bottom: 1px solid #ccc;
            padding-bottom: 5px;
        }
        .linha {
            font-size: 18px;
            margin-bottom: 0.4cm;
        }
    </style>
</head>
<body>
    <div class="etiqueta">
        <div class="titulo">📦 REMETENTE</div>
        <div class="linha">Nome: {{ remetente }}</div>
        <div class="linha">Endereço: {{ endereco_remetente }}</div>
        <div class="linha">Transportadora: {{ transportadora }}</div>
        <div class="linha">Mercadoria: Livro</div>
    </div>

    <div class="etiqueta">
        <div class="titulo">🚚 DESTINATÁRIO</div>
        <div class="linha">Nome: {{ destinatario }}</div>
        <div class="linha">Endereço: {{ endereco_destinatario }}</div>
        <div class="linha">Transportadora: {{ transportadora }}</div>
        <div class="linha">Mercadoria: Livro</div>
    </div>
</body>
</html>
'''

FORM_TEMPLATE = '''
<!DOCTYPE html>
<html lang="pt">
<head>
    <meta charset="UTF-8">
    <title>Gerador de Etiquetas</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f4f4f4;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .form-container {
            background-color: #ffffff;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            width: 100%;
            max-width: 500px;
        }
        h2 {
            text-align: center;
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 8px;
            font-weight: 500;
        }
        input[type="text"] {
            width: 100%;
            padding: 10px;
            margin-bottom: 20px;
            border: 1px solid #ccc;
            border-radius: 5px;
        }
        button {
            width: 100%;
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 12px;
            font-size: 16px;
            border-radius: 5px;
            cursor: pointer;
        }
        button:hover {
            background-color: #45a049;
        }
    </style>
</head>
<body>
    <div class="form-container">
        <h2>Gerar Etiqueta de Envio</h2>
        <form method="post">
            <label>Remetente:</label>
            <input type="text" name="remetente" required>

            <label>Endereço Remetente:</label>
            <input type="text" name="endereco_remetente" required>

            <label>Destinatário:</label>
            <input type="text" name="destinatario" required>

            <label>Endereço Destinatário:</label>
            <input type="text" name="endereco_destinatario" required>

            <label>Transportadora:</label>
            <input type="text" name="transportadora">

            <button type="submit">Gerar Etiqueta (PDF)</button>
        </form>
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        rendered = render_template_string(
            HTML_TEMPLATE,
            remetente=request.form['remetente'],
            endereco_remetente=request.form['endereco_remetente'],
            destinatario=request.form['destinatario'],
            endereco_destinatario=request.form['endereco_destinatario'],
            transportadora=request.form['transportadora']
        )

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as pdf_file:
            HTML(string=rendered).write_pdf(pdf_file.name)
            return send_file(pdf_file.name, as_attachment=True, download_name="etiqueta.pdf")

    return FORM_TEMPLATE

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
