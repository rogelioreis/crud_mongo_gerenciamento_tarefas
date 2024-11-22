from model.tarefas import Tarefa
from model.usuarios import Usuario
from reports.relatorios import Relatorio
from controller.controller_usuario import Controller_Usuario
from conexion.mongo_queries import MongoQueries
import pandas as pd
from datetime import datetime

class Controller_Tarefa:
    def __init__(self):
        self.ctrl_usuario = Controller_Usuario()
        self.relatorio = Relatorio()
        self.mongo = MongoQueries() 
        

    def inserir_tarefa(self) -> Tarefa:

        self.mongo.connect()
        
        self.listar_usuarios()

        usuario_cpf = str(input("Digite o CPF do Usuário responsável pela tarefa: "))
        usuario = self.valida_usuario(usuario_cpf)
        if usuario is None:
            return None
        
        titulo = str(input("Digite o titulo da tarefa: "))
        descricao = str(input("Digite a descrição da tarefa: "))
        data_criacao = int(datetime.now().timestamp() * 1000)

        # Gera o próximo código de tarefa incremental
        ultimo_codigo = self.mongo.db['tarefas'].find_one(
            sort=[("codigo_tarefa", -1)],  # Ordena por código de tarefa em ordem decrescente
            projection={"codigo_tarefa": 1}
        )
        novo_codigo_tarefa = (ultimo_codigo["codigo_tarefa"] + 1) if ultimo_codigo else 1

        nova_tarefa = {
            "codigo_tarefa": novo_codigo_tarefa,
            "titulo": titulo,
            "descricao": descricao,
            "data_criacao": data_criacao,
            "data_conclusao": None,  
            "status": 0,  # Status 0 para tarefa pendente
            "cpf": usuario.get_CPF(),
        }

        resultado = self.mongo.db['tarefas'].insert_one(nova_tarefa)
        nova_tarefa["_id"] = resultado.inserted_id

        # Recupera a tarefa inserida
        tarefa_inserida = Tarefa(
            codigo_tarefa=nova_tarefa["codigo_tarefa"],
            titulo=nova_tarefa["titulo"],
            descricao=nova_tarefa["descricao"],
            data_criacao=nova_tarefa["data_criacao"],
            usuario=usuario
        )

        print(tarefa_inserida.to_string())
        self.mongo.close()

        return tarefa_inserida

    def atualizar_tarefa(self) -> Tarefa:

        self.mongo.connect()

        self.listar_tarefas()

        codigo_tarefa = int(input("Código da Tarefa que irá alterar: "))        

        # Verifica se a tarefa existe
        tarefa_atual = self.mongo.db['tarefas'].find_one({"codigo_tarefa": codigo_tarefa})
        if tarefa_atual is None:
            print(f"O código {codigo_tarefa} não existe.")
            return None

        if tarefa_atual["status"] == 1:
            print("Não é possível atualizar uma tarefa que já foi concluída.")
            return None
        
        print()
        print("1 - Alterar dados")
        print("2 - Concluir tarefa")
        print("0 - Sair")
        escolha = int(input("Escolha uma opção [0 - 2]: "))

        if escolha == 1:

            print()
            self.listar_usuarios()
            usuario_cpf = str(input("Digite o CPF do Usuário responsável pela tarefa: "))
            usuario = self.valida_usuario(usuario_cpf)

            if usuario is None:
                return None

            novo_titulo = str(input("Digite o novo titulo da tarefa: "))
            nova_descricao = str(input("Digite a nova descrição da tarefa: "))
            
            data_criacao = int(datetime.now().timestamp() * 1000)

            # Atualiza a tarefa no MongoDB
            self.mongo.db['tarefas'].update_one(
                {"codigo_tarefa": codigo_tarefa},
                {
                    "$set": {
                        "titulo": novo_titulo,
                        "descricao": nova_descricao,
                        "data_criacao": data_criacao,
                        "cpf": usuario.get_CPF()
                    }
                }
            )

            tarefa_atualizada = Tarefa(
                codigo_tarefa=codigo_tarefa,
                titulo=novo_titulo,
                descricao=nova_descricao,
                data_criacao=data_criacao,
                usuario=usuario
            )

            print(tarefa_atualizada.to_string())
            self.mongo.close()
            return tarefa_atualizada
            
        elif escolha == 2:

            data_conclusao_atual = int(datetime.now().timestamp() * 1000)
            # Conclui a tarefa
            self.mongo.db['tarefas'].update_one(
                {"codigo_tarefa": codigo_tarefa},
                {"$set": {"status": 1, "data_conclusao": data_conclusao_atual}}
            )

            # Atualiza a tarefa concluída
            tarefa_atualizada = self.mongo.db['tarefas'].find_one({"codigo_tarefa": codigo_tarefa})
            usuario_cpf = tarefa_atualizada["cpf"]
            usuario = self.valida_usuario(usuario_cpf)

            tarefa_concluida = Tarefa(
                codigo_tarefa=codigo_tarefa,
                titulo=tarefa_atualizada["titulo"],
                descricao=tarefa_atualizada["descricao"],
                data_criacao=tarefa_atualizada["data_criacao"],
                data_conclusao=tarefa_atualizada["data_conclusao"],
                status=1,
                usuario=usuario
            )

            print(tarefa_concluida.to_string())
            self.mongo.close()
            return tarefa_concluida

        else:
            self.mongo.close()
            return None

    def excluir_tarefa(self):

        self.mongo.connect()

        self.listar_tarefas()

        codigo_tarefa = int(input("Código da Tarefa que irá excluir: "))        

        # Verifica se a tarefa existe
        tarefa_atual = self.mongo.db['tarefas'].find_one({"codigo_tarefa": codigo_tarefa})
        if tarefa_atual is None:
            self.mongo.close()
            print(f"O código {codigo_tarefa} não existe.")
            return

        opcao_excluir = input(f"Tem certeza que deseja excluir a tarefa {codigo_tarefa} [S ou N]: ")
        if opcao_excluir.lower() == "s":
            
            self.mongo.db['tarefas'].delete_one({"codigo_tarefa": codigo_tarefa})
            self.mongo.close()
            print("Tarefa removida com sucesso!")

    def listar_usuarios(self):
        self.relatorio.get_relatorio_usuarios()

    def listar_tarefas(self):
        self.relatorio.get_relatorio_tarefas()

    def valida_usuario(self, usuario_cpf: str) -> Usuario:
        usuario = self.mongo.db['usuarios'].find_one({"cpf": usuario_cpf})
        if usuario is None:
            print(f"O CPF {usuario_cpf} informado não existe na base.")
            return None
        else:
            return Usuario(usuario['cpf'], usuario['nome'])
