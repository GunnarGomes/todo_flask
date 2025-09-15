from flask import Flask, flash, redirect, url_for, render_template
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from cadastro.cad_usr import bp_cadastro_usuario
from auth.login import bp_login
from todo.routes import bp_todo
import os

load_dotenv()

def create_app():
    app = Flask(__name__)
    jwt_key = os.getenv("JWT_KEY")
    app.secret_key = jwt_key
    app.config["JWT_SECRET_KEY"] = jwt_key
    app.config["JWT_TOKEN_LOCATION"] = ["cookies"]  # usar só cookie
    app.config["JWT_COOKIE_SECURE"] = False  # True se estiver em HTTPS
    app.config["JWT_COOKIE_SAMESITE"] = "Lax"
    app.config["JWT_COOKIE_CSRF_PROTECT"] = False  # simplificação para testes
    jwt = JWTManager(app)
    
    #
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        flash("Sua sessão expirou. Faça login novamente.", "warning")
        return redirect(url_for("bp_login.Login"))  # endpoint do seu login

    @jwt.invalid_token_loader
    def invalid_token_callback(error_string):
        flash("Token inválido. Faça login novamente.", "warning")
        return redirect(url_for("bp_login.Login"))

    @jwt.unauthorized_loader
    def missing_token_callback(error_string):
        flash("Você precisa fazer login para acessar esta página.", "warning")
        return redirect(url_for("bp_login.Login"))
    
    app.register_blueprint(bp_cadastro_usuario)
    app.register_blueprint(bp_login)
    app.register_blueprint(bp_todo)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)