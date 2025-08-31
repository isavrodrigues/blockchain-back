from flask import Flask, render_template
import json
from datetime import datetime

app = Flask(__name__)

def load_data(filename):
    with open(f'data/{filename}.json', 'r', encoding='utf-8') as f:
        return json.load(f)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/sobre")
def sobre():
    # Carrega os dados da equipe para usar na página "Sobre"
    time_data = load_data('time')
    return render_template("sobre.html", time=time_data)

@app.route("/eventos")
def eventos():
    eventos_data = load_data('eventos')
    hoje = datetime.now().date()
    
    # Separa os eventos com base na data
    eventos_futuros = [e for e in eventos_data if datetime.strptime(e['data'], '%Y-%m-%d').date() >= hoje]
    eventos_passados = [e for e in eventos_data if datetime.strptime(e['data'], '%Y-%m-%d').date() < hoje]
    
    return render_template("eventos.html", futuros=eventos_futuros, passados=eventos_passados)

@app.route("/conteudo")
def conteudo():
    # Carrega e separa o conteúdo em Blog e Bibliografia
    conteudo_data = load_data('conteudo')
    blog_posts = [c for c in conteudo_data if c['tipo'] == 'blog']
    bibliografia_items = [c for c in conteudo_data if c['tipo'] == 'bibliografia']
    return render_template("conteudo.html", blog=blog_posts, bibliografia=bibliografia_items)

@app.route("/contato")
def contato():
    return render_template("contato.html")


if __name__ == "__main__":
    app.run(debug=True)