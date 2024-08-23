# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 08:31:52 2024
@author: Drew.Bennett
http://127.0.0.1:8000/
http://127.0.0.1:8000/static/index.html
"""


#from typing import Union
from fastapi import FastAPI,HTTPException,Request,Form,Body,Depends,Response
from fastapi.staticfiles import StaticFiles
#from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse#,HTMLResponse#,RedirectResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

import asyncpg
from contextlib import asynccontextmanager

from os.path import dirname
from os import path
from dataclasses import dataclass

from pydantic import BaseModel
from typing import Annotated, Union
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
import jwt

import json

@dataclass
class Job:
    job_number:str = Form()
    client:str = Form()
    project:str = Form()
    
    

DB_USER = 'postgres'
DB_PASSWORD = 'pts21'
DB_HOST = 'localhost'
DB_NAME = 'cores_app'
#context manager to close connection pool after use
@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.pool = await asyncpg.create_pool(user=DB_USER, password=DB_PASSWORD,database=DB_NAME, host=DB_HOST)
    yield
    await app.state.pool.close()




pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def hash_password(password: str):
    return "fakehashed" + password
    return pwd_context.hash(password)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login",auto_error=False)



#def verify_token(token:str):#unprocessabe entity
#return True if token signature ok.
def verify_token(token: str = Depends(oauth2_scheme)):
    token = str(token)
    print('token',token)#object ?!
   # return True
    try:
     #   t = json.loads(token)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return True
    except jwt.PyJWTError as e:
        print(e)
        raise HTTPException(status_code=401, detail="Invalid token")



app = FastAPI(lifespan=lifespan)
frontend_folder = dirname(dirname(__file__))
app.mount(r"/static", StaticFiles(directory=path.join(frontend_folder,"javascript_only")), name="static")
#would be nice to have this at root. can't seem to do this.
#templates = Jinja2Templates(directory=path.join(frontend_folder,"jinga2templates"))



SECRET_KEY = "09d25e094faa6ca2556c818166b7b9563b93f7099f6c0f4cfa6ef63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
@app.post("/login")
async def create_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> str:
    #More secure to not reveal if username exists. Use same error message.
    err = HTTPException(status_code=400, detail="Incorrect username or password")
    async with app.state.pool.acquire() as con:
        result = await con.fetchrow('select username,hashed_password from users where username = $1', form_data.username)
    if result is not None:
        hashed_password = hash_password(form_data.password)
        if hashed_password == result['hashed_password']:
            expires = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            to_encode = {'user':result['username'],'expires':expires.isoformat()}
            token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
            return token
         #   return {"access_token": token, "token_type": "Bearer"} 
    raise err



@app.get("/get_job_numbers",response_class = JSONResponse)
async def get_job_numbers():
    async with app.state.pool.acquire() as con:
        result = await con.fetch('select job_number from job order by job_number')
        return [r[0] for r in result]



#{job_number,project,client}
@app.get("/get_job_details",response_class = JSONResponse)
async def get_job_details(job_number:str = '' , token : str = Depends(verify_token)):
    async with app.state.pool.acquire() as con:
        result = await con.fetchrow('select job_number,project,client from job where job_number = $1', job_number)
        if result is None:
            return {'job_number':'','project':'','client':''}
            #raise HTTPException(status_code=404, detail='job_number {} not found'.format(job_number))
        else:
            return dict(result.items())



#{project,client}
@app.post("/add_job/")
#async def add_job(job_number: Annotated[str, Form()],client: Annotated[str, Form()],project: Annotated[str, Form()]):
async def add_job(j: Job = Depends()):    
    job_number = j.job_number
    client = j.client
    project = j.project
    async with app.state.pool.acquire() as con:
        try:
            await con.execute('insert into job(job_number,client,project) values ($1,$2,$3)',job_number,client,project)
            return {'job_number':str(job_number),'client':str(client),'project':str(project),'error':''}
        except Exception as e:
            return {'job_number':'','client':'','project':'','error':str(e)}
        


#{project,client}
@app.post("/update_job/{old_job_number}")
async def update_job(old_job_number:str,j:Job = Depends()):
    async with app.state.pool.acquire() as con:
        await con.execute('update job set job_number = $1,client=$2,project=$3 where job_number = $4',j.job_number,j.client,j.project,old_job_number)
        return 'Updated job. Number = {}, client = {},project = {}'.format(str(j.job_number),str(j.client),str(j.project))
        


#{project,client}
@app.delete("/delete_job/{job_number}")
async def delete_job(request: Request,job_number:str):
    async with app.state.pool.acquire() as con:
        await con.execute('delete from job where job_number = $1',job_number)
    return 'deleted job {}'.format(job_number)

