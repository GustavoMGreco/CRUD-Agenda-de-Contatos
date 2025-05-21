from flask import Flask, render_template, request, redirect, url_for
import pymysql

app = Flask(__name__)


def conectar():
    return pymysql.connect(
        host='localhost',
        user='user',
        password='12345',
        database='agenda',
        cursorclass=pymysql.cursors.DictCursor
    )

def listarContatos():
    conexao = conectar()
    with conexao:
        with conexao.cursor() as cursor:
            cursor.execute('SELECT * FROM contatos')
            return cursor.fetchall()

def adicionarContato(dados):
    conexao = conectar()
    with conexao:
        with conexao.cursor() as cursor:
            cursor.execute('INSERT INTO contatos(nome, telefone, email) VALUES (%s, %s, %s)', (dados['nome'], dados['telefone'], dados['email']))
            conexao.commit()

def buscarContato(id):
    conexao = conectar()
    with conexao:
        with conexao.cursor() as cursor:
            cursor.execute('SELECT * FROM contatos WHERE id = %s', (id,))
            contato = cursor.fetchone()
            return contato

def editarContato(id, dados):
    conexao = conectar()
    with conexao:
        with conexao.cursor() as cursor:
            cursor.execute('UPDATE contatos SET nome=%s, telefone=%s, email=%s WHERE id=%s', (dados['nome'], dados['telefone'], dados['email'], id))
            conexao.commit()
            return cursor.rowcount

def excluirContato(id):
    conexao = conectar()
    with conexao:
        with conexao.cursor() as cursor:
            cursor.execute('DELETE FROM contatos WHERE id = %s', (id,))
            conexao.commit()
            return cursor.rowcount


@app.route('/')
def listar():
    contatos = listarContatos()
    return render_template('index.html', contatos=contatos)

@app.route('/novo')
def novoContato():
    return render_template('formulario.html', contato={})

@app.route('/adicionar', methods=['POST'])
def adicionar():
    dados = {
        'nome': request.form['nome'],
        'telefone': request.form['telefone'],
        'email': request.form['email']
    }
    adicionarContato(dados)
    return redirect(url_for('listar'))

@app.route('/editar/<int:id>')
def editar(id):
    contato = buscarContato(id)
    return render_template('formulario.html', contato=contato)

@app.route('/atualizar/<int:id>', methods=['POST'])
def atualizar(id):
    dados = {
        'nome': request.form['nome'],
        'telefone': request.form['telefone'],
        'email': request.form['email']
    }
    editarContato(id, dados)
    return redirect(url_for('listar')) 

@app.route('/excluir/<int:id>')
def excluir(id):
    excluirContato(id)
    return redirect(url_for('listar'))


if __name__ == '__main__':
    app.run(debug=True)
