from fastapi import FastAPI, Body
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn
import json
from pydantic import BaseModel
# import tts_stt as text_speech
import db_handler as dbh
import os.path

#db_table_name = 'Commands'
glob_path = os.path.abspath(os.getcwd())


app = FastAPI()
@app.get("/")
def root():
    return FileResponse(glob_path+"\\server\\front\\index.html")
app.mount("/static", StaticFiles(directory=glob_path+"\\server\\front"), name="static")


@app.get('/favicon.ico')
def set_favicon():
    return FileResponse(glob_path+"\\server")


@app.get('/REST/{data_base_name}/{db_table_name}')
def get_db(data_base_name: str, db_table_name:str):
    db = dbh.create_or_connect_to_db(glob_path+'\\'+data_base_name)
    curs = dbh.create_cursor(db)
    dbh.update_db(db)
    items = dbh.read_from(db,curs,db_table_name)
    respouse = []
    for i in items:
        respouse.append(
            {
                'id': i[0],
                'voice_comand':i[1],
                'action_type':i[2],
                'command':i[3],
                'timestapm':i[4],
            }
        )
    dbh.delete_cursor(curs)
    return respouse

@app.get('/REST/{data_base_name}/{db_table_name}/{some_column}/{some_id}')
def get_line_form_db(data_base_name: str,  db_table_name:str, some_column:str, some_id:str):
    db = dbh.create_or_connect_to_db(glob_path+'\\'+data_base_name)
    curs = dbh.create_cursor(db)
    dbh.update_db(db)
    items = dbh.read_from_by_column(db,curs,db_table_name,some_column,some_id)
    respouse = []
    for i in items:
        respouse.append(
            {
                'id': i[0],
                'voice_comand':i[1],
                'action_type':i[2],
                'command':i[3],
                'timestapm':i[4],
            }
        )
    dbh.delete_cursor(curs)
    return respouse
    #return #return line from db by id

#TODO this is a bad example you need to scale this function
@app.post('/REST/{data_base_name}/{db_table_name}/add/{voice_comand}/{action_type}/{command}/{timestapm}')
def post_line_into_db(data_base_name :str, db_table_name:str,voice_comand:str,action_type:str,command:str,timestapm:str ):    
    db = dbh.create_or_connect_to_db(glob_path+'\\'+data_base_name)
    curs = dbh.create_cursor(db)
    dbh.update_db(db)
    try:
        dbh.insert_into(db,curs,db_table_name,[voice_comand,action_type,command,timestapm])
    except Exception as e:
        return {f'Error cant insert data, {e}'} 
    
    dbh.delete_cursor(curs)
    return f'item {voice_comand}, {action_type}, {command}, {timestapm} has been added sucsessfully'
    

@app.delete('/REST/{data_base_name}/{db_table_name}/del/{some_id}')
def del_line_from_db_by_id(data_base_name: str, db_table_name:str,some_id:str):
    db = dbh.create_or_connect_to_db(glob_path+'\\'+data_base_name)
    curs = dbh.create_cursor(db)
    dbh.update_db(db)
    try:
        dbh.delete_from_by_id(db,curs,db_table_name,some_id)
    except Exception as e:
        return {f'Error cant delete data, {e}'} 
    dbh.delete_cursor(curs)
    return f'item with id {some_id} has been deleted sucsessfully'


def start_server():
    uvicorn.run("server.back.server:app", host="127.0.0.1", reload=True)




