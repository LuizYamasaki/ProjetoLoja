from flask import Flask, render_template, request, redirect, session
import sqlite3 as sql
import uuid

app = Flask(__name__)
app.secret_key = "quitandadozezinho"

usuario = "Zé da Manga"
senha = "1234"
login = False

# ------------------------------ FUNÇÃO PARA VERIFICAR A SESSÃO ------------------------------

def verifica_sessao():
    if "login" in session and session["login"]:
        return True
    else:
        return False
    
# -------------- ROTA DA PÁGINA LOGIN --------------
@app.route("/login")
def login():
    return render_template("login.html")
    
# -------------------- ROTA PARA VERIFICAR O ACESSO AO ADMIN --------------------
@app.route("/acesso", methods=['POST'])
def acesso():
    global usuario, senha
    usuario_informado = request.form["usuario"]
    senha_informada = request.form["senha"]

    if usuario == usuario_informado and senha == senha_informada:
        session["login"] = True
        return redirect('/')
    else:
        return render_template("login.html",msg="O usuário e a sua senha estão INCORRETOS!!")
    
# ------------------------------ CONEXÃO COM O BANCO DE DADOS ------------------------------

def conecta_database():
    conexao = sql.connect("db_quitanda.db")
    conexao.row_factory = sql.Row
    return conexao

# ------------------------------ INICIAR O BANCO DE DADOS ------------------------------

def iniciar_db():
    conexao = conecta_database()
    with app.open_resource('esquema.sql', mode='r') as comandos:
        conexao.cursor().executescript(comandos.read())
        conexao.commit()
        conexao.close()

# ------------------------------ ROTA DA PÁGINA INICIAL ------------------------------

@app.route("/")
def index():
    iniciar_db()
    conexao = conecta_database()
    produtos = conexao.execute('SELECT * FROM produtos ORDER BY id_prod DESC').fetchall()
    conexao.close()
    title = "Home"
    return render_template("home.html", produtos=produtos, title=title)


# ------------------------------ FINAL DO CODIGO - EXECUTANDO O SERVIDOR ------------------------------

app.run(debug=True)
