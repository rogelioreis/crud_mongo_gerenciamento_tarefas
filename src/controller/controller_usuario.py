from model.usuarios import Usuario
from conexion.mongo_queries import MongoQueries

class Controller_Usuario:
    def __init__(self):
        pass

    def inserir_usuario(self) -> Usuario:
        mongo = MongoQueries()
        mongo.connect()

        cpf = input("CPF (Novo): ")

        if not self.verifica_existencia_usuario(mongo, cpf):
            nome = input("Nome (Novo): ")
            # Insere
            mongo.db["usuarios"].insert_one({"cpf": cpf, "nome": nome})
            # Recupera os dados do novo usuário
            df_usuario = self.recupera_usuario(mongo, cpf)
            # Cria um novo objeto Usuario
            novo_usuario = Usuario(df_usuario["cpf"], df_usuario["nome"])
            # Exibe os atributos do novo usuário
            print("Usuário Inserido com Sucesso!")
            print(novo_usuario.to_string())
            return novo_usuario
        else:
            print(f"O CPF {cpf} já está cadastrado.")
            return None

    def atualizar_usuario(self) -> Usuario:
        mongo = MongoQueries()
        mongo.connect()
        self.listar_usuarios(mongo)
        cpf = input("CPF do usuário que deseja alterar o nome: ")

        # Verifica se o usuário existe
        if self.verifica_existencia_usuario(mongo, cpf):
            novo_nome = input("Nome (Novo): ")
            # Atualiza o nome do usuário existente
            mongo.db["usuarios"].update_one({"cpf": cpf}, {"$set": {"nome": novo_nome}})
            # Recupera os dados do usuário atualizado
            df_usuario = self.recupera_usuario(mongo, cpf)
            # Cria um novo objeto Usuario
            usuario_atualizado = Usuario(df_usuario["cpf"], df_usuario["nome"])
            # Exibe os atributos do usuário atualizado
            print(usuario_atualizado.to_string())
            return usuario_atualizado
        else:
            print(f"O CPF {cpf} não existe.")
            return None

    def excluir_usuario(self):
        mongo = MongoQueries()
        mongo.connect()
        self.listar_usuarios(mongo)
        cpf = input("CPF do Usuário que irá excluir: ")

        if self.verifica_existencia_usuario(mongo, cpf):
            if self.verifica_vinculo_tarefa(mongo, cpf):
                print(f"O usuário com CPF {cpf} não pode ser excluído porque está vinculado a uma ou mais tarefas!")
            else:
                df_usuario = self.recupera_usuario(mongo, cpf)
                opcao_excluir = input(f"Tem certeza que deseja excluir o usuario {cpf} [S ou N]: ")
                if opcao_excluir.lower() == "s":
                    # Remove o usuário da tabela
                    mongo.db["usuarios"].delete_one({"cpf": cpf})
                    usuario_excluido = Usuario(df_usuario["cpf"], df_usuario["nome"])
                    print("Usuário Removido com Sucesso!")
                    print(usuario_excluido.to_string())
        else:
            print(f"O CPF {cpf} não existe.")

    def listar_usuarios(self, mongo: MongoQueries):
        query = list(mongo.db["usuarios"].find({}, {"_id": 0, "cpf": 1, "nome": 1}))
        if query:
            for usuario in query:
                print(usuario)
        else:
            print("Nenhum usuário encontrado.")

    def verifica_existencia_usuario(self, mongo: MongoQueries, cpf: str) -> bool:
        query = mongo.db["usuarios"].find_one({"cpf": cpf})
        return query is not None

    def verifica_vinculo_tarefa(self, mongo: MongoQueries, cpf: str) -> bool:
        count = mongo.db["tarefas"].count_documents({"cpf": cpf})
        return count > 0

    def recupera_usuario(self, mongo: MongoQueries, cpf: str) -> dict:
        usuario = mongo.db["usuarios"].find_one({"cpf": cpf}, {"_id": 0, "cpf": 1, "nome": 1})
        if usuario:
            return usuario
        return {}
