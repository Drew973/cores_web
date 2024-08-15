# -*- coding: utf-8 -*-
"""
Created on Mon Aug 12 09:37:06 2024

@author: Drew.Bennett
"""

from dataclasses import dataclass,fields
from fastapi import Form

from crud_template_maker import writeForm


@dataclass
class Job:
    job_number:str = Form()
    client:str = Form()
    project:str = Form()
    
    
@dataclass
class Core:
    job_number:str = Form()#foreign key
    core_number:int = Form()
    sec:str = Form()
    chainage:float = Form()
    
    
    
    
#print(asdict(Job))
#t = {field.name: str(field.type) for field in fields(Job)}
r = writeForm(fields(Core),'Core')
print(r)