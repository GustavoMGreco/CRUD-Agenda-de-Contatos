from flask import Flask
import pymysql

app = Flask(__name__)

def conectar():
    return pymysql.connect(
        host='localhost',
        user='user',
        password='12345',
        database='Agenda',
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route('/')
def listarContatos():
    return

def adicionarContato():
    return

def editarContato():
    return

def buscarContato():
    return

def excluirContato():
    return
