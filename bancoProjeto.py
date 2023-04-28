import psycopg2
from psycopg2 import Error
from projeto import Projeto
import datetime

class BancoProjeto:

    # Construtor da classe BancoProjeto, com a definição do atributo __conn (conexão com banco de dados) 
    def __init__(self):
        self.__conn = None
    
    # Abre uma conexão com o banco de dados
    def abrir(self):
        self.__conn = psycopg2.connect(user="postgres", password="123456", host="127.0.0.1", port="5432", database="projetos")

    # Fecha a conexão com o banco de dados
    def fechar(self):
        if (self.__conn):
            self.__conn.close()

    # Recebe um objeto Projeto sem ID e salva no banco de dados.
    def salvar(self, projeto):
        try:
            self.abrir()
            cursor = self.__conn.cursor()
            cursor.execute("insert into projetos (nome, descricao, criado_em, atualizado_em) values (%s, %s, %s, %s)",
            (projeto.nome, projeto.descricao, str(datetime.datetime.now()), str(datetime.datetime.now()),))
            self.__conn.commit()
        except (Exception, Error) as error:
            print("Erro ao salvar o projeto")
        finally:
            self.fechar()

    # Recebe um objeto Projeto com ID e atualiza seus dados no banco
    def atualizar(self, projeto):
        try:
            self.abrir()
            cursor = self.__conn.cursor()
            cursor.execute("update projetos set nome=%s, descricao=%s, criado_em=%s, atualizado_em=%s where id=%s",
            (projeto.nome, projeto.descricao, projeto.criadoEm, str(datetime.datetime.now()), projeto.id))
            self.__conn.commit()
        except (Exception, Error) as error:
            print("Erro ao atualizar o projeto")
        finally:
            self.fechar()

    # Deleta um Projeto a partir de seu ID
    def excluir(self, id):
        try:
            self.abrir()
            cursor = self.__conn.cursor()
            cursor.execute("delete from projetos where id=%s", (id,))
            self.__conn.commit()
        except (Exception, Error) as error:
            print("Erro ao excluir o projeto", error)
        finally:
            self.fechar()

    # Busca um Projeto a partir de seu ID
    def buscarPorId(self, id):
        projeto = None
        try:
            self.abrir()
            cursor = self.__conn.cursor()
            cursor.execute("select * from projetos where id=%s", (id,))
            registro = cursor.fetchone()
            id = registro[0]
            nome = registro[1]
            descricao = registro[2]
            criadoEm = registro[3]
            atualizadoEm = registro[4]
            projeto = Projeto(id, nome, descricao, criadoEm, atualizadoEm)
        except (Exception, Error) as error:
            print("Erro ao buscar projeto")
        finally:
            self.fechar()
        return projeto

    # Lista todos os Projetos que estão salvos no banco
    def listar(self):
        projetos = []
        try:
            self.abrir()
            cursor = self.__conn.cursor()
            cursor.execute("select * from projetos")
            registros = cursor.fetchall()
            for linha in registros:
                id = linha[0]
                nome = linha[1]
                descricao = linha[2]
                criadoEm = linha[3]
                atualizadoEm = linha[4]
                projeto = Projeto(id, nome, descricao, criadoEm, atualizadoEm)
                projetos.append(projeto)
        except (Exception, Error) as error:
            print("Erro ao listar projetos")
        finally:
            self.fechar()
        return projetos