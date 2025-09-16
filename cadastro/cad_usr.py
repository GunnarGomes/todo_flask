from flask import Blueprint, request, redirect, render_template
from database.models import Usuario, engine
from sqlalchemy.orm import sessionmaker
from werkzeug.security import generate_password_hash

Session = sessionmaker(bind=engine)
session = Session()

bp_cadastro_usuario = Blueprint("bp_cadastro_usuario",__name__,template_folder="templates",static_folder="static")

@bp_cadastro_usuario.route("/cadastro")
def Cadastro_view():
    return render_template("cadastro.html")

@bp_cadastro_usuario.route("/cadastrar", methods=["POST"])
def Cadastrar():
    nome = request.form.get("nome")
    email = request.form.get("email")
    senha = request.form.get("senha")
    
    senha_hash = generate_password_hash(senha)
    
    if not nome or not email or not senha:
        return "Todos os campos são obrigatórios!", 400
    
    new_usr = Usuario(nome=nome,email=email,senha=senha_hash)
    session.add(new_usr)
    session.commit()
    return "Cadastro feito com sucesso"