# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 08:31:52 2024
@author: Drew.Bennett
http://127.0.0.1:8000/
http://127.0.0.1:8000/static/index.html
"""


#from typing import Union
from fastapi import FastAPI,HTTPException,Request,Form,Body,Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse,HTMLResponse#,RedirectResponse

import asyncpg
from contextlib import asynccontextmanager
import logging
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer

from os.path import dirname
from os import path
from dataclasses import dataclass

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)
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


app = FastAPI(lifespan=lifespan)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


frontend_folder = dirname(dirname(__file__))
app.mount(r"/static", StaticFiles(directory=path.join(frontend_folder,"javascript_only")), name="static")
#would be nice to have this at root. can't seem to do this.

templates = Jinja2Templates(directory=path.join(frontend_folder,"jinga2templates"))


fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}



@dataclass
class Job:
    job_number:str = Form()
    client:str = Form()
    project:str = Form()
    
    
    
def fake_hash_password(password: str):
    return "fakehashed" + password

    
    
    
@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    
    
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
        
        
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}

    
    


@app.get("/get_job_numbers",response_class = JSONResponse)
async def get_job_numbers():
    async with app.state.pool.acquire() as con:
        result = await con.fetch('select job_number from job order by job_number')
        return [r[0] for r in result]



#{job_number,project,client}
@app.get("/get_job_details",response_class = JSONResponse)
async def get_job_details(job_number:str = ''):
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
    #logger.debug('get_jobs')
    
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
#async def update_job(old_job_number:str,job_number: Annotated[str, Form()],client: Annotated[str, Form()],project: Annotated[str, Form()]):
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

