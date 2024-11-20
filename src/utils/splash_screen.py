from conexion.mongo_queries import MongoQueries

class SplashScreen:
    def __init__(self, mongo_queries):
        self.mongo_queries = mongo_queries

    def contar_documentos(self, collection_name):
        # Conta documentos em uma coleção
        return self.mongo_queries.db[collection_name].count_documents({})  

    def exibir(self):
        usuarios = self.contar_documentos("usuarios")  # Nome da coleção de usuários no MongoDB
        tarefas = self.contar_documentos("tarefas")    # Nome da coleção de tarefas no MongoDB

        print("###############################################")
        print("#                                             #")
        print("#      SISTEMA DE GERENCIAMENTO DE TAREFAS    #")
        print("#                                             #")
        print("###############################################")
        print("#                                             #")
        print("#  TOTAL DE REGISTROS EXISTENTES              #")
        print(f"#  1 - USUÁRIOS: {usuarios:<5}")
        print(f"#  2 - TAREFAS: {tarefas:<5}")
        print("#                                             #")
        print("#                                             #")
        print("#  CRIADO POR:                                #")
        print("#  Rogelio Soares Reis Filho                  #")
        print("#  Murilo da Silva Soares                     #")
        print("#  Jordhan Fernandes de Assis                 #")
        print("#  Mariana Lopes Ferreira                     #")
        print("#                                             #")
        print("#  DISCIPLINA: BANCO DE DADOS 2024/2          #")
        print("#  PROFESSOR: HOWARD ROATTI                   #")
        print("#                                             #")
        print("###############################################")


if __name__ == "__main__":
    mongo_queries = MongoQueries()
    mongo_queries.connect()  
    try:
        splash_screen = SplashScreen(mongo_queries)  
        splash_screen.exibir()  
    finally:
        mongo_queries.close()


