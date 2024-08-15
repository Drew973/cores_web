# -*- coding: utf-8 -*-
"""
Created on Thu Aug  8 14:47:36 2024

@author: Drew.Bennett





writes html form and javascript functions to console.


form displays single row of data. 
select chooses which row.
    add new thing... option changes legend and submit button.
    

model:pydantic model

backend needs entry points like: 
    update_thing(old_pk,formData)
    add_thing(thing)
    delete_thing(pk)
    get_thing(pk)
    get_thing_keys()
"""




import typing


def write_template(model):
    pass



'''
 <FORM id = "core_form">
			<fieldset class = 'edit_fieldset'>
			<legend id = 'coreLegend'>Edit Job </legend>
			<p><button id = 'submitButton' onclick = 'submitJob()'>Add</button></p>
			</fieldset>
			 </FORM>
'''


def writeForm(model,name:str) -> str:
    
    inputs = ''
    for field in model:
        
        if str(field.type) == "<class 'str'>":#better way to do this?            
            inputs += '<p><label for = "{n}">{n}:<input type="text" name="{n}" id="{n}"></label></p>\n'.format(n = field.name)
            
        if str(field.type) == "<class 'float'>":#better way to do this?            
            inputs += '<p><label for = "{n}">{n}:<input type="number" name="{n}" id="{n}"></label></p>\n'.format(n = field.name)  
            
        if str(field.type) == "<class 'int'>":#better way to do this?            
            inputs += '<p><label for = "{n}">{n}:<input type="number" step=1 name="{n}" id="{n}"></label></p>\n'.format(n = field.name)  
            

            
    return '''<FORM id = "{name}form">
   			<fieldset class = 'editFieldset'>
   			<legend id = '{name}Legend'>Edit {name} </legend>
            {inputs}
   			<p><button id = 'submitButton' onclick = 'submitJob()'>Add</button></p>
   			</fieldset>
   			 </FORM>'''.format(inputs = inputs,name = name)
    
    

    
    
    
    
    