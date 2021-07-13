import uvicorn
import json
import random
import pytz
import requests
import os
from bson.objectid import ObjectId
from typing import Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

"""Datetime"""
BRT = pytz.timezone("America/Sao_Paulo")

"""Config"""
with open("config.json","r") as fp:
    conf = json.load(fp)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def insert_video_db(text, voice, actor, video_name, video_id):
    try:
        dict_insert_video = {
            "name" : video_name,
            "video_id" : video_id,
            "actor" : actor,
            "voice" : voice,
            "text" : text,
            "create_date" : datetime.now().astimezone(BRT),
            "done" : False,
            "url" : None
        }
        insert_video = db.videos.insert_one(dict_insert_video)
        return True
    except:
        return False

class post_video(BaseModel):
    text: str
    voice: str
    actor: str
    video_name: str


@app.get("/")
def read_root():
    return {"data": "root api"}


@app.get("/ttfs_video")
def ttfs_video(video_id: str):
        try:
            permission = db.pessoas.find_one({
            "passcode": passcode })
            cliente = db.infos.find_one({"client": "Procempa"})
            termos = cliente.get("termos_de_uso")
            dados = cliente.get("dados_armazenados")

            if permission:
                return {"data" : {
                    "permission" : permission.get("permission"),
                    "termos_de_uso" : termos,
                    "dados_armazenados" : dados
                }}
            else:
                return {"data" : {"error" : "Nenhum cadastro de pessoa encontrado"}}
        except:
            return {"data" :  {"error" : "Passcode Inválido, tente novamente"}}

@app.post("/create_ttfs")
def create_ttfs(request: post_video):
    video_id = str(ObjectId())
    if True:
        try:
            prompt_command = f'python action.py --name "{video_id}" --text "{request.text}"'
            os.system(prompt_command)
            return {'data' : {
                "url" : f"D:/_DigitalPages/DeepFake/Videos-Personalizados/results/ttfs/{video_id}.mp4"
            }}
        except:
            return {'data' : f"Houve um problema na produção do vídeo"}
    else:
        return {'data' : f"Há um problema na conexão do Banco de Dados"}


if __name__ == "__main__":
    uvicorn.run(app,host="127.0.0.1",port=9000)