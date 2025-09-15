from sqlalchemy import create_engine, Integer, String, Column, DateTime, ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from dotenv import load_dotenv
import os
load_dotenv()
sql_url = os.getenv("SQL_URL")

engine = create_engine(sql_url)
Base = declarative_base()

class Usuario(Base):
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(48), nullable=False)
    email = Column(String(256), nullable=False)
    senha = Column(String(256), nullable=False)
    data_criacao = Column(DateTime(timezone=True), server_default=func.now())
    
    tarefas = relationship("Tarefa", back_populates="usuario", cascade="all, delete")
    projetos = relationship("Projeto", back_populates="usuario", cascade="all, delete")

class Projeto(Base):
    __tablename__ = "projetos"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE")) 
    titulo = Column(String(38), nullable=False)
    
    usuario = relationship("Usuario", back_populates="projetos")
    tarefas = relationship("Tarefa", back_populates="projeto", cascade="all, delete")

class Tarefa(Base):
    __tablename__ = "tarefas"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"))
    projeto_id = Column(Integer, ForeignKey("projetos.id", ondelete="CASCADE"))
    titulo = Column(String(48), nullable=False)
    descricao = Column(String(100))
    
    usuario = relationship("Usuario", back_populates="tarefas")
    projeto = relationship("Projeto", back_populates="tarefas")

Base.metadata.create_all(engine)