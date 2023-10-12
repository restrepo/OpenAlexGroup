'''
$ sudo pip3 install fastapi
$ pip3 install uvicorn[standard]
$ uvicorn main:app --reload
'''
from typing import Optional

from fastapi import FastAPI
from starlette.responses import FileResponse ###
from starlette.staticfiles import StaticFiles ###


import requests

import json

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static") ###

file='https://api.openalex.org/sources?filter=concept.id:C109214941,apc_usd:0'

#JSON SCHEME
#[{"student_id": str,
# "Evaluation 1":{"value": int,
#                 "%": int,
#                 "Description": str
#                 }, 
# ...
# }
#]

@app.get("/")
def read_item(student_id: str = "", output: str = "html"):
    '''
    You can write the API documentation here:
    
    For example: 
    
    USAGE: http://127.0.0.1:8000/?student_id=1113674432
    '''
    #Real time JSON file
    r=requests.get(file)
    rr=r.json().get('results')
    db=[{'id': 'https://openalex.org/S173952182', 'issn_l': '0370-2693'},{'id': 'https://openalex.org/S173952182', 'issn_l': '0370-2693'}]
    print('***',db)
    new_db=[ d for d in db if d.get('student_id')==student_id  ]
    f=open('static/data/filtered.json','w')
    if not student_id:
    	json.dump(db,f)
    else:
    	json.dump(new_db,f)
    f.close()

    if output == 'json':
        if not student_id:
    	    return db
        else:
    	    return new_db
    else:
        return FileResponse('index.html')
