import logging
from conexion.mongo_queries import MongoQueries
from conexion.oracle_queries import OracleQueries
import pandas as pd
import json

LIST_OF_COLLECTIONS = ["tarefas", "usuarios"]
logger = logging.getLogger(name="Crud_Mongo_Gerenciamento_Tarefas")
logger.setLevel(level=logging.WARNING)
mongo = MongoQueries()

def createCollections(drop_if_exists:bool=False):
    mongo.connect()
    existing_collections = mongo.db.list_collection_names()
    for collection in LIST_OF_COLLECTIONS:
        if collection in existing_collections:
            if drop_if_exists:
                mongo.db.drop_collection(collection)
                logger.warning(f"{collection} droped!")
                mongo.db.create_collection(collection)
                logger.warning(f"{collection} created!")
        else:
            mongo.db.create_collection(collection)
            logger.warning(f"{collection} created!")
    mongo.close()

def insert_many(data:json, collection:str):
    mongo.connect()
    mongo.db[collection].insert_many(data)
    mongo.close()

def extract_and_insert():
    oracle = OracleQueries()
    oracle.connect()
    sql = "select * from labdatabase.{table}"
    
    for collection in LIST_OF_COLLECTIONS:
        df = oracle.sqlToDataFrame(sql.format(table=collection))
        
        if collection == "tarefas":
            
            df["data_criacao"] = pd.to_datetime(df["data_criacao"], errors='coerce')
            df["data_conclusao"] = pd.to_datetime(df["data_conclusao"], errors='coerce')

        logger.warning(f"Data extracted from Oracle database: labdatabase.{collection}")
        
        # Converte o DataFrame para JSON
        records = json.loads(df.T.to_json()).values()
        logger.warning("Data converted to JSON format")
        
        # Insere os registros no MongoDB
        insert_many(data=records, collection=collection)
        logger.warning(f"Documents inserted into {collection} collection")


if __name__ == "__main__":
    logging.warning("Starting")
    createCollections(drop_if_exists=True)
    extract_and_insert()
    logging.warning("End")
