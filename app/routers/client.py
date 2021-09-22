"""Client Route."""

from fastapi import APIRouter, Depends, HTTPException,Request, Form
from typing import List
from pydantic import BaseModel

from ..dependencies import get_token_header
from ..gdb.services import client


class Client(BaseModel):
    id : str
    status : bool
    name : str
    houseNumber : int
    location : str
    password : str
    JobSheet: List[ str ] = []
    class Config:
        '''Docstring here.'''
        schema_extra = {
            "example": {
                "id": "7f644301-e3f1-4752-90d5-99fbfad91ab3",
                "status" : True,
                "name" : 'John Doe',
                "houseNumber" : 23,
                "location" : "DT1 1SS",
                "password" : "Secret_Pa55w0rd",
                "JobSheet": ["79dc3d3a-c40b-47e8-8cf4-207c2de7e36","c85a5633-2803-4826-ae5a-82474c238d5","0348ae36-202a-4bfc-a92d-849607fd541" ],
            }
        }


router = APIRouter(
    prefix="/clients",
    tags=["clients"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

def find_client(ref):
    if ref not in fake_clients_db:
        raise HTTPException(status_code=404, detail="Customers not found")
    return {"result": fake_clients_db[ref]}


fake_clients_db = {"7f644301-e3f1-4752-90d5-99fbfad91ab3": {
    "id": "7f644301-e3f1-4752-90d5-99fbfad91ab3",
    "status" : True,
    "name" : 'John Doe',
    "houseNumber" : 23,
    "location" : "DT1 1SS",
    "password" : "Secret_Pa55w0rd",
    "signup_ts": None,
    "JobSheet": ["79dc3d3a-c40b-47e8-8cf4-207c2de7e36","c85a5633-2803-4826-ae5a-82474c238d5","0348ae36-202a-4bfc-a92d-849607fd541" ]
}, "7f644301-e3f1-4752-90d5-99fbfad91ab4": {
    "id": "7f644301-e3f1-4752-90d5-99fbfad91ab4",
    "status" : True,
    "name" : 'Jane Doe',
    "houseNumber" : 33,
    "location" : "DT2 2SS",
    "password" : "Secret_Pa55w0rd",
    "signup_ts": None,
    "JobSheet": ["79dc3d3a-c40b-47e8-8cf4-207c2de7e24","c85a5633-2803-4826-ae5a-82474c238c4","0348ae36-202a-4bfc-a92d-849607fd520" ]
}}


@router.get("/")
async def get_clients():
    resp = client.get_all_clients()
    return resp

@router.post("/register/")
async def register_client(data: Client ):
    return {"name": data.name, "clients_id": data.id, "location": data.location}


@router.get("/{clients_id}")
async def read_clients(clients_id: str ):
    resp = client.get_client_profile(clients_id)
    print(f"Client : {resp}")
    return {clients_id: resp["profile"]}


@router.put(
    "/{clients_id}",
    tags=["custom"],
    responses={403: {"description": "Operation forbidden"}},
)
async def update_clients(clients_id: str):
    if clients_id != "plumbus":
        raise HTTPException(
            status_code=403, detail="You can only update the item: plumbus"
        )
    return {"clients_id": clients_id, "name": "The great Plumbus"}


def create_client(customer: Client):
    pass