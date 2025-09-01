from flask import Flask, render_template, request
import json, os
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

@app.route("/contato", methods=["GET", "POST"])
def contato():
    if request.method == "POST":
        payload = {
            "nome": request.form.get("nome", "").strip(),
            "email": request.form.get("email", "").strip(),
            "mensagem": request.form.get("mensagem", "").strip(),
            "timestamp": datetime.now().isoformat(timespec="seconds")
        }
        os.makedirs("data", exist_ok=True)
        path = "data/contatos.json"
        try:
            with open(path, "r", encoding="utf-8") as f:
                db = json.load(f)
        except FileNotFoundError:
            db = []
        db.append(payload)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(db, f, ensure_ascii=False, indent=2)

        return render_template("contato.html", submitted=True, nome=payload["nome"])
    return render_template("contato.html", submitted=False)


if __name__ == "__main__":
    app.run(debug=True)
