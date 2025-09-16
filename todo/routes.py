from flask import Blueprint, request, redirect, render_template, flash,jsonify, url_for
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.orm import sessionmaker
from database.models import Tarefa, Projeto, engine

Session = sessionmaker(bind=engine)
session = Session()

bp_todo = Blueprint("bp_todo",__name__,template_folder="templates",static_folder="static")

@bp_todo.route("/tasks/<int:id_projeto>",methods=["GET","POST"])
@jwt_required()
def Todo(id_projeto):
    identity = get_jwt_identity()
    to_dos = session.query(Tarefa).filter_by(usuario_id=int(identity),projeto_id=id_projeto).all()
    return render_template("todo.html", todo=to_dos, projeto_id=id_projeto)

@bp_todo.route("/tasks",methods=["GET"])
@jwt_required()
def Projetos():
    identity = get_jwt_identity()
   
    projetos = session.query(Projeto).filter_by(usuario_id=int(identity)).all()
    print(f"id:{identity}")
    print(projetos)
    return render_template("tasks.html", projetos=projetos)

@bp_todo.route("/api/create_task/<int:projeto_id>",methods=["GET","POST"])
@jwt_required()
def Create_task(projeto_id):
    identity = get_jwt_identity()
    if request.method == "POST":
        titulo = request.form.get("titulo")
        descricao = request.form.get("descricao")
    
    new_task = Tarefa(usuario_id=int(identity),projeto_id=projeto_id,titulo=titulo,descricao=descricao)
    try:
        session.add(new_task)
        session.commit()
    except Exception as e:
        session.rollback()  # limpa a sessão
        flash(f"Erro ao criar tarefa: {e}", "error")   
    return redirect(url_for("bp_todo.Todo", id_projeto=projeto_id))

@bp_todo.route("/api/create_project",methods=["GET","POST"])
@jwt_required()
def Create_project():
    identity = get_jwt_identity()
    if request.method == "POST":
        titulo = request.form.get("titulo")
    
    new_projeto = Projeto(usuario_id=int(identity),titulo=titulo)
    try:
        session.add(new_projeto)
        session.commit()
    except Exception as e:
        session.rollback()  # limpa a sessão
        flash(f"Erro ao criar projeto: {e}", "error")   
    return redirect(url_for("bp_todo.Projetos"))