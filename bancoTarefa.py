import psycopg2
from psycopg2 import Error
from tarefa import Tarefa
from projeto import Projeto
import datetime

class BancoTarefa:
    
    # Construtor da classe BancoTarefa, com a definição do atributo __conn (conexão com banco de dados) 
    def __init__(self):
        self.__conn = None
    
    # Abre uma conexão com o banco de dados
    def abrir(self):
        self.__conn = psycopg2.connect(user="postgres", password="123456", host="127.0.0.1", port="5432", database="projetos")
    
    # Fecha a conexão com o banco de dados
    def fechar(self):
        if (self.__conn):
            self.__conn.close()

    # Recebe um objeto Tarefa sem ID e salva no banco de dados.
    def salvar(self, tarefa):
        try:
            self.abrir()
            cursor = self.__conn.cursor()
            cursor.execute("""insert into tarefas 
                    (projeto_id, nome, descricao, concluido, notas, prazo, criado_em, atualizado_em) 
                values (%s, %s, %s, %s, %s, %s, %s, %s)""",
            (tarefa.projeto.id, tarefa.nome, tarefa.descricao, tarefa.concluido,
                tarefa.notas, tarefa.prazo, str(datetime.datetime.now()), str(datetime.datetime.now()),))
            self.__conn.commit()
        except (Exception, Error) as error:
            print("Erro ao salvar a tarefa")
        finally:
            self.fechar()

    # Recebe um objeto Tarefa com ID e atualiza seus dados no banco
    def atualizar(self, tarefa):
        try:
            self.abrir()
            cursor = self.__conn.cursor()
            cursor.execute("""update tarefas 
                set projeto_id=%s, nome=%s, descricao=%s, concluido=%s, notas=%s, prazo=%s, criado_em=%s, atualizado_em=%s 
                where id=%s""",
            (tarefa.projeto.id, tarefa.nome, tarefa.descricao, tarefa.concluido, tarefa.notas,
                tarefa.prazo, tarefa.criadoEm, str(datetime.datetime.now()), tarefa.id,))
            self.__conn.commit()
        except (Exception, Error) as error:
            print("Erro ao atualizar a tarefa")
        finally:
            self.fechar()

    # Deleta uma tarefa a partir de seu ID
    def excluir(self, id):
        try:
            self.abrir()
            cursor = self.__conn.cursor()
            cursor.execute("delete from tarefas where id=%s", (id,))
            self.__conn.commit()
        except (Exception, Error) as error:
            print("Erro ao excluir a tarefa", error)
        finally:
            self.fechar()

    # Busca uma Tarefa a partir de seu ID
    def buscarPorId(self, id):
        tarefa = None
        try:
            self.abrir()
            cursor = self.__conn.cursor()
            cursor.execute("""select t.id, t.nome, t.descricao, t.concluido, t.notas, 
                t.prazo, t.criado_em, t.atualizado_em, t.projeto_id, p.nome 
                from tarefas t
                join projetos p on t.projeto_id = p.id 
                where t.id=%s""", (id,))
            registro = cursor.fetchone()
            id = registro[0]
            nome = registro[1]
            descricao = registro[2]
            concluido = registro[3]
            notas = registro[4]
            prazo = registro[5]
            criadoEm = registro[6]
            atualizadoEm = registro[7]
            idProjeto = registro[8]
            nomeProjeto = registro[9]
            projeto = Projeto(idProjeto, nomeProjeto, None, None, None)
            tarefa = Tarefa(id, projeto, nome, descricao, concluido, notas, prazo, criadoEm, atualizadoEm)
        except (Exception, Error) as error:
            print("Erro ao buscar tarefa")
        finally:
            self.fechar()
        return tarefa

    # Lista todas as Tarefas que estão salvas no banco
    def listar(self, projetoId):
        tarefas = []
        try:
            self.abrir()
            cursor = self.__conn.cursor()
            if (projetoId):
                cursor.execute("""select t.id, t.nome, t.descricao, t.concluido, t.notas, 
                t.prazo, t.criado_em, t.atualizado_em, t.projeto_id, p.nome, p.descricao, 
                p.criado_em, p.atualizado_em  
                from tarefas t
                join projetos p on t.projeto_id = p.id 
                where t.projeto_id=%s 
                order by p.nome asc, t.prazo asc""", (projetoId,))
            else:
                cursor.execute("""select t.id, t.nome, t.descricao, t.concluido, t.notas, t.prazo, 
                t.criado_em, t.atualizado_em, t.projeto_id, p.nome, p.descricao, p.criado_em, 
                p.atualizado_em  
                from tarefas t
                join projetos p on t.projeto_id = p.id 
                order by p.nome asc, t.prazo asc""")
            registros = cursor.fetchall()
            for registro in registros:
                id = registro[0]
                nome = registro[1]
                descricao = registro[2]
                concluido = registro[3]
                notas = registro[4]
                prazo = registro[5]
                criadoEm = registro[6]
                atualizadoEm = registro[7]
                idProjeto = registro[8]
                nomeProjeto = registro[9]
                descricaoProjeto = registro[10]
                projetoCriadoEm = registro[11]
                projetoAtualizadoEm = registro[12]
                print(projetoAtualizadoEm)
                projeto = Projeto(idProjeto, nomeProjeto, descricaoProjeto, projetoCriadoEm, projetoAtualizadoEm)
                
                tarefa = Tarefa(id, projeto, nome, descricao, concluido, notas, prazo, criadoEm, atualizadoEm)
                tarefas.append(tarefa)
        except (Exception, Error) as error:
            print("Erro ao listar tarefas")
        finally:
            self.fechar()
        return tarefas