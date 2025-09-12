from pymongo import MongoClient


try:
    client = MongoClient("mongodb://localhost:27017/")
    db = client['macrofauna']
except Exception as ex:
    print(f"Erro ao se conectar ao banco: {ex}")
