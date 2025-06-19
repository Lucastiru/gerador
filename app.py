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
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 2cm;
            background: #f8f8f8;
            display: flex;
            flex-direction: column;
            gap: 2cm;
        }
        .etiqueta {
            width: 18cm;
            border: 2px dashed #000;
            padding: 1cm;
            background: #fff;
            border-radius: 12px;
            box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
        }
        .titulo {
            font-size: 1.5em;
            font-weight: bold;
            margin-bottom: 0.5em;
            border-bottom: 1px solid #ccc;
            padding-bottom: 0.3em;
        }
        .linha {
            font-size: 1.1em;
            margin-bottom: 0.4em;
        }
        .info {
            font-weight: bold;
            color: #333;
        }
    </style>
</head>
<body>
    <div class="etiqueta">
        <div class="titulo">📦 REMETENTE</div>
        <div class="linha info">{{ remetente }}</div>
        <div class="linha">{{ endereco_remetente }}</div>
        <div class="linha">Transportadora: <strong>{{ transportadora }}</strong></div>
        <div class="linha">Mercadoria: <strong>Livro</strong></div>
    </div>
    <div class="etiqueta">
        <div class="titulo">🚚 DESTINATÁRIO</div>
        <div class="linha info">{{ destinatario }}</div>
        <div class="linha">{{ endereco_destinatario }}</div>
        <div class="linha">Transportadora: <strong>{{ transportadora }}</strong></div>
        <div class="linha">Mercadoria: <strong>Livro</strong></div>
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
</head>
<body>
    <h2>Gerar Etiqueta de Envio</h2>
    <form method="post">
        <label>Remetente: <input type="text" name="remetente" required></label><br><br>
        <label>Endereço Remetente: <input type="text" name="endereco_remetente" required></label><br><br>
        <label>Destinatário: <input type="text" name="destinatario" required></label><br><br>
        <label>Endereço Destinatário: <input type="text" name="endereco_destinatario" required></label><br><br>
        <label>Transportadora: <input type="text" name="transportadora"></label><br><br>
        <button type="submit">Gerar Etiqueta (PDF)</button>
    </form>
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
