from conexion.mongo_queries import MongoQueries
import pandas as pd
from pymongo import ASCENDING, DESCENDING

class Relatorio:
    def __init__(self):
        pass

    def get_relatorio_tarefas(self):
        mongo = MongoQueries()
        mongo.connect()
        query_result = mongo.db["tarefas"].aggregate([
                                                    {
                                                        '$project': {
                                                            'codigo_tarefa': 1,
                                                            'titulo': 1,
                                                            'descricao': 1,
                                                            'data_criacao': 1,
                                                            'data_conclusao': 1,
                                                            'status': {
                                                                '$switch': {
                                                                    'branches': [
                                                                        {'case': {'$eq': ['$status', 0]}, 'then': 'Pendente'},
                                                                        {'case': {'$eq': ['$status', 1]}, 'then': 'Concluída'}
                                                                    ],
                                                                    'default': 'Outro'
                                                                }
                                                            },
                                                            'cpf': 1,
                                                            '_id': 0
                                                        }
                                                    },
                                                    {'$sort': {'data_criacao': ASCENDING}}
                                                ])
        df_tarefas = pd.DataFrame(list(query_result))

        df_tarefas['data_criacao'] = pd.to_datetime(df_tarefas['data_criacao'], unit = 'ms')
        df_tarefas['data_conclusao'] = pd.to_datetime(df_tarefas['data_conclusao'], unit = 'ms')

        df_tarefas['data_criacao'] = df_tarefas['data_criacao'].apply(lambda x: str(x).split('.')[0])
        df_tarefas['data_conclusao'] = df_tarefas['data_conclusao'].apply(lambda x: str(x).split('.')[0])

        mongo.close()
        print(df_tarefas)
        


    def get_relatorio_tarefas_concluidas(self):
        mongo = MongoQueries()
        mongo.connect()
        query_result = mongo.db["tarefas"].aggregate([
                                                    {'$match': {'status': 1}},
                                                    {
                                                        '$lookup': {  # Faz o join com a coleção de usuários
                                                            'from': 'usuarios',
                                                            'localField': 'cpf',
                                                            'foreignField': 'cpf',
                                                            'as': 'usuario'
                                                        }
                                                    },
                                                    {'$unwind': '$usuario'},  
                                                    {
                                                        '$project': {  # Projeta os campos necessários
                                                            'codigo_tarefa': 1,
                                                            'titulo': 1,
                                                            'descricao': 1,
                                                            'data_criacao': 1,
                                                            'data_conclusao': 1,
                                                            'tempo_gasto': {
                                                                '$subtract': ['$data_conclusao', '$data_criacao']
                                                            },  
                                                            'usuario': '$usuario.nome',
                                                            'cpf': 1,
                                                            '_id': 0
                                                        }
                                                    },
                                                    {'$sort': {'data_conclusao': 1}}  
                                                ])
    
        # Converte o resultado em DataFrame para exibição
        df_tarefas_concluidas = pd.DataFrame(list(query_result))

        df_tarefas_concluidas['data_criacao'] = pd.to_datetime(df_tarefas_concluidas['data_criacao'], unit = 'ms')
        df_tarefas_concluidas['data_conclusao'] = pd.to_datetime(df_tarefas_concluidas['data_conclusao'], unit = 'ms')

        df_tarefas_concluidas['tempo_gasto'] = pd.to_timedelta(df_tarefas_concluidas['tempo_gasto'] / 1000, unit='s')

        df_tarefas_concluidas['data_criacao'] = df_tarefas_concluidas['data_criacao'].apply(lambda x: str(x).split('.')[0])
        df_tarefas_concluidas['data_conclusao'] = df_tarefas_concluidas['data_conclusao'].apply(lambda x: str(x).split('.')[0])
        df_tarefas_concluidas['tempo_gasto'] = df_tarefas_concluidas['tempo_gasto'].apply(lambda x: str(x).split('.')[0])

        mongo.close()
    
        print(df_tarefas_concluidas)
        


    def get_relatorio_tarefas_por_usuario(self):
        mongo = MongoQueries()
        mongo.connect()
        query_result = mongo.db["usuarios"].aggregate([
                                                    {
                                                        '$lookup': {
                                                            'from': 'tarefas',
                                                            'localField': 'cpf',
                                                            'foreignField': 'cpf',
                                                            'as': 'tarefas'
                                                        }
                                                    },
                                                    {
                                                        '$project': {
                                                            'nome': 1,
                                                            'total_tarefas': {'$size': '$tarefas'},
                                                            '_id': 0
                                                        }
                                                    },
                                                    {'$sort': {'total_tarefas': DESCENDING}}
                                                ])
        df_tarefas_usuario = pd.DataFrame(list(query_result))
        mongo.close()
        print(df_tarefas_usuario)
        

    def get_relatorio_usuarios(self):
        mongo = MongoQueries()
        mongo.connect()
        query_result = mongo.db["usuarios"].find({},
                                                 {"cpf": 1,
                                                  "nome": 1,
                                                  "_id": 0
                                                 }).sort("nome", ASCENDING)
        df_usuarios = pd.DataFrame(list(query_result))
        mongo.close()
        print(df_usuarios)
        
