# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 12:48:50 2024

@author: Drew.Bennett
"""

from fastapi import FastAPI
import logging
import sys

logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)

app = FastAPI()

@app.get("/")
async def root():
    logger.debug('this is a debug message')
    return {"message": "basic Hello World"}