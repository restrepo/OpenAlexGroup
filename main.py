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



@app.get("/")
def read_item(concept: str = "", output: str = "html"):
    '''
    You can write the API documentation here:
    
    For example: 
    
    USAGE: http://127.0.0.1:8000/?concept=particle+physics
    '''
    #Real time JSON file:
    concept_id=''
    if concept:
        print('va 1')
        concept_id='concept.id:C109214941,'
    else:
        print('va 2')
        
    file=f'https://api.openalex.org/sources?filter={concept_id}apc_usd:0'
    
    r=requests.get(file)
    rr=r.json().get('results')
    maxj=100
    db=[
        { 
          'journal'   : d.get('display_name'),
          'publisher' : d.get('host_organization_name'),
          'articles'  : f"{d.get('works_count'):,}",
          'citations' : f"{d.get('cited_by_count'):,}",
          'h_index'   : d.get('summary_stats').get('h_index')
         } for d in rr[:maxj]
    ]
    print('*',concept,'*',db)
    f=open('static/data/filtered.json','w')
    json.dump(db,f)
    f.close()

    if output == 'json':
        # http://127.0.0.1:8000/?concept=particle+physics&output=json
        return db
    else:
        # http://127.0.0.1:8000/?concept=particle+physics
        return FileResponse('index.html')
