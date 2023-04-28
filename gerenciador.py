from flask import Flask, render_template, request, redirect
import psycopg2
from psycopg2 import Error
from bancoProjeto import BancoProjeto
from bancoTarefa import BancoTarefa
from projeto import Projeto
from tarefa import Tarefa

app = Flask(__name__)

@app.route('/')
def index():
    projetos = BancoProjeto().listar()
    return render_template('projetos/lista.html', lista = projetos)

@app.route('/projetos/novo')
def cadastrarProjeto():
    return render_template('projetos/form.html', titulo='Novo projeto')

@app.route('/projetos/<int:id>/editar')
def editarProjeto(id):
    projetoExistente = BancoProjeto().buscarPorId(id)
    tarefas = BancoTarefa().listar(id)
    if (projetoExistente):
        return render_template('/projetos/edit.html', titulo='Editando projeto', projeto=projetoExistente, tarefas=tarefas)
    return redirect('/')

@app.route('/projetos/criar', methods=["POST",])
def salvarProjeto():
    nome = request.form['nome']
    descricao = request.form['descricao']
    projeto = Projeto(None, nome, descricao, None, None)    
    BancoProjeto().salvar(projeto)
    return redirect('/')

@app.route('/projetos/atualizar', methods=["POST",])
def atualizarProjeto():
    id = request.form['id']
    nome = request.form['nome']
    descricao = request.form['descricao']
    criadoEm = request.form['criadoEm']
    projeto = Projeto(id, nome, descricao, criadoEm, None)
    BancoProjeto().atualizar(projeto)
    return redirect('/')

@app.route('/projetos/<int:id>/excluir')
def excluirProjeto(id):
    BancoProjeto().excluir(id)
    return redirect('/')

@app.route('/tarefas')
def listarTarefas():
    tarefas = BancoTarefa().listar(None)
    return render_template('tarefas/lista.html', lista = tarefas)

@app.route('/tarefas/novo')
def cadastrarTarefa():
    projetos = BancoProjeto().listar()
    return render_template('tarefas/form.html', titulo='Novo Tarefa', projetos=projetos)

@app.route('/tarefas/<int:id>/editar')
def editarTarefa(id):
    tarefaExistente = BancoTarefa().buscarPorId(id)
    projetos = BancoProjeto().listar()
    if (tarefaExistente):
        return render_template('/tarefas/edit.html', tarefa=tarefaExistente, projetos=projetos)
    return redirect('/tarefas')

@app.route('/tarefas/<int:id>/excluir')
def excluirTarefa(id):
    BancoTarefa().excluir(id)
    return redirect('/tarefas')

@app.route('/tarefas/criar', methods=["POST",])
def salvarTarefa():
    nome = request.form['nome']
    descricao = request.form['descricao']
    prazo = request.form['prazo']
    idProjeto = request.form['idProjeto']
    notas = request.form['notas']
    projeto = Projeto(idProjeto, None, None, None, None)
    tarefa = Tarefa(None, projeto, nome, descricao, False, notas, prazo, None, None)    
    BancoTarefa().salvar(tarefa)
    return redirect('/tarefas')

@app.route('/tarefas/atualizar', methods=["POST",])
def atualizarTarefa():
    idTarefa = request.form['id']
    nome = request.form['nome']
    descricao = request.form['descricao']
    prazo = request.form['prazo']
    idProjeto = request.form['idProjeto']
    notas = request.form['notas']
    criadoEm = request.form['criadoEm']
    concluido = 'concluido' in request.form
    projeto = Projeto(idProjeto, None, None, None, None)
    print(concluido)
    tarefa = Tarefa(idTarefa, projeto, nome, descricao, concluido, notas, prazo, criadoEm, None)
    BancoTarefa().atualizar(tarefa)
    return redirect('/tarefas')

app.run(debug=True)