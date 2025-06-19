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
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; }
        .etiqueta {
            width: 15cm; height: 10cm;
            border: 1px solid #000; padding: 1cm;
        }
        .secao { margin-bottom: 1cm; }
        .titulo { font-weight: bold; font-size: 1.2em; margin-bottom: 0.5em; }
        .linha { margin-bottom: 0.3em; }
    </style>
</head>
<body>
    <div class="etiqueta">
        <div class="secao">
            <div class="titulo">REMETENTE</div>
            <div class="linha">{{ remetente }}</div>
            <div class="linha">{{ endereco_remetente }}</div>
        </div>
        <div class="secao">
            <div class="titulo">DESTINATÁRIO</div>
            <div class="linha">{{ destinatario }}</div>
            <div class="linha">{{ endereco_destinatario }}</div>
        </div>
        {% if observacao %}<div class="linha"><em>{{ observacao }}</em></div>{% endif %}
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
        <label>Observação (opcional): <input type="text" name="observacao"></label><br><br>
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
            observacao=request.form['observacao']
        )
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as pdf_file:
            HTML(string=rendered).write_pdf(pdf_file.name)
            return send_file(pdf_file.name, as_attachment=True, download_name="etiqueta.pdf")
    return FORM_TEMPLATE

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))