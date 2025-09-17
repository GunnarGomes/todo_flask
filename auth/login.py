from flask import Blueprint, request, redirect, render_template, jsonify, make_response
from flask_jwt_extended import create_access_token, set_access_cookies
from database.models import Usuario, engine
from sqlalchemy.orm import sessionmaker
from werkzeug.security import check_password_hash

Session = sessionmaker(bind=engine)
session = Session()

bp_login = Blueprint("bp_login", __name__, template_folder="templates",static_folder="static")

@bp_login.route("/login", methods=["GET","POST"])
def Login():
    return render_template("login.html")

@bp_login.route("/api/login",methods=["GET","POST"])
def Logar():
    email = request.args.get("email")
    senha = request.args.get("senha")
    
    if not email or not senha:
        return "calma lá paizão, ta faltando dados, bota ai vai"
    
    usuario = session.query(Usuario).filter_by(email=email).first()
    
    if usuario and check_password_hash(usuario.senha, senha):
        token = create_access_token(identity=str(usuario.id),additional_claims={
            "email": usuario.email,
            "nome": usuario.nome
        })
        resp = make_response(redirect("/tasks"))
        set_access_cookies(resp, token)  # salva o JWT num cookie HttpOnly
        
        return resp
        
    else:
        return "errado paizão"
        
    
    