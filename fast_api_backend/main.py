# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 08:31:52 2024
@author: Drew.Bennett
http://127.0.0.1:8000/
http://127.0.0.1:8000/static/index.html
"""


from typing import Union
from fastapi import FastAPI,HTTPException,Request,Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from fastapi.responses import JSONResponse,HTMLResponse#,RedirectResponse

import asyncpg
from contextlib import asynccontextmanager
import logging
from typing import Annotated



logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)
DB_USER = 'postgres'
DB_PASSWORD = 'pts21'
DB_HOST = 'localhost'
DB_NAME = 'cores_app'



#context manager to close connections after use
@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.pool = await asyncpg.create_pool(user=DB_USER, password=DB_PASSWORD,database=DB_NAME, host=DB_HOST)
    yield
    await app.state.pool.close()


app = FastAPI(lifespan=lifespan)
app.mount(r"/static", StaticFiles(directory=r"C:\Users\drew.bennett\Documents\cores_app\frontend\javascript_only"), name="static")
#would be nice to have this at root. can't seem to do this.

templates = Jinja2Templates(directory=r"C:\Users\drew.bennett\Documents\cores_app\frontend\jinga2templates")



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





#{job_number,project,client}
@app.get("/get_job_table/{job_number}",response_class = HTMLResponse)
async def get_job_table(request: Request, job_number:str = ''):
    async with app.state.pool.acquire() as con:
        result = await con.fetchrow('select job_number,project,client from job where job_number = $1', job_number)
        if result is None:
            return 'Unable to find job number: "{jn}"'.format(jn = job_number)
            #raise HTTPException(status_code=404, detail='job_number {} not found'.format(job_number))
        else:
            return templates.TemplateResponse(request=request, name="job.html", context = dict(result.items()))



@app.get("/get_job_numbers",response_class = JSONResponse)
async def get_job_numbers():
    async with app.state.pool.acquire() as con:
        result = await con.fetch('select job_number from job order by job_number')
        return [r[0] for r in result]



#{project,client}
@app.post("/update_job/{old_job_number}")
async def update_job(old_job_number:str,job_number: Annotated[str, Form()],client: Annotated[str, Form()],project: Annotated[str, Form()]):
    #logger.debug('get_jobs')
    async with app.state.pool.acquire() as con:
        await con.execute('update job set job_number = $1,client=$2,project=$3 where job_number = $4',job_number,client,project,old_job_number)
        return 'Updated job. Number = {}, client = {},project = {}'.format(str(job_number),str(client),str(project))
        


#{project,client}
@app.delete("/delete_job/{job_number}")
async def delete_job(request: Request,job_number:str):
    details = {'job_number':job_number}
    #logger.debug('get_jobs')
    async with app.state.pool.acquire() as con:
        await con.execute('delete from job where job_number = $1',job_number)
      #  return 'deleted job {}'.format(job_number)
    return templates.TemplateResponse(request=request, name="deleted_job.html", context=details)


#{project,client}
@app.post("/add_job")
async def add_job(job_number: Annotated[str, Form()],client: Annotated[str, Form()],project: Annotated[str, Form()]):
    #logger.debug('get_jobs')
    async with app.state.pool.acquire() as con:
        try:
            await con.execute('insert into job(job_number,client,project) values ($1,$2,$3)',job_number,client,project)
            return {'job_number':str(job_number),'client':str(client),'project':str(project),'error':''}
        except Exception as e:
            return {'job_number':'','client':'','project':'','error':str(e)}
        





#if __name__ == "__main__":
   #uvicorn.run(app, host="0.0.0.0", port=8000)

