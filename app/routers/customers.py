"""Customer Route."""

from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

from ..dependencies import get_token_header
from ..gdb.services import customer

class Customer(BaseModel):
    id: str
    status : bool
    title : str
    CompanyReg : int
    RegisteredAddress : str
    password : str
    signup_ts: Optional[datetime] = None
    AreasCovered: List[ str ] = []
    WorkingDays: List[ str ] = []
    services: List[ str ] = []
    class Config:
        '''Docstring here.'''
        schema_extra = {
            "example": {
                "id": "9g644301-e3f1-4752-90d5-99fbfad99xy4",
                "status" : True,
                "title" : 'Any Clean',
                "CompanyReg" : 7999999,
                "RegisteredAddress" : "1 Main Street, Anytown, Anycounty, Anyland, XX9 9XX",
                "password" : "Secret_Pa55w0rd",
                "signup_ts": None,
                "AreasCovered":["DT1", "DT2"],
                "WorkingDays":[1,2,3,4,5,6],
                "services": [1,3,4],
            }}

router = APIRouter(
    prefix="/customers",
    tags=["customers"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

def find_customer(ref):
    if ref not in fake_customers_db:
        raise HTTPException(status_code=404, detail="Customer not found")
    return {"result": fake_customers_db[ref]}


fake_customers_db = { "9g644301-e3f1-4752-90d5-99fbfad99xy4": {
                "id": "9g644301-e3f1-4752-90d5-99fbfad99xy4",
                "status" : True,
                "title" : 'ServiceMaster',
                "CompanyReg" : 7999999,
                "RegisteredAddress" : "The Cleaning Centre, Groove Trading Estate, Dorchester DT1 1ST",
                "password" : "Secret_Pa55w0rd",
                "signup_ts": None,
                "AreasCovered":["DT1", "DT2", "DT3", "DT4", "DT5", "DT9", "DT10", "DT11"],
                "WorkingDays":[1,2,3,4,5,6],
                "services": [1,3,4],
            },
     "9g644301-e3f1-4752-90d5-99fbfad99dc9":{
                "id": "9g644301-e3f1-4752-90d5-99fbfad99dc9",
                "status" : True,
                "title" : 'Cloverclean',
                "CompanyReg" : 7888888,
                "RegisteredAddress" : "27 Oakwood, Broadmayne, Dorchester DT2 8UL",
                "password" : "Secret_Pa55w0rd",
                "signup_ts": None,
                "AreasCovered":["DT1", "DT2", "DT3", "DT4", "DT5", "DT6", "DT7", "DT8"],
                "WorkingDays":[1,2,3,4,5],
                "services": [1,2,5]
            }}


@router.get("/")
async def get_customers():
    resp = customer.get_all_customers()
    return resp


@router.post("/register/")
async def register_customer(data: Customer ):
    return {"name": data.name, "clients_id": data.id, "location": data.location}


@router.get("/{customers_id}")
async def read_customers(customers_id: str):
    resp = customer.get_customer_profile(customers_id)
    print(f"Client : {resp}")
    return {customers_id: resp["profile"]}

@router.put(
    "/{customers_id}",
    tags=["custom"],
    responses={403: {"description": "Operation forbidden"}},
)
async def update_customer(customers_id: str):
    if customers_id != "plumbus":
        raise HTTPException(
            status_code=403, detail="You can only update the customers: plumbus"
        )
    return {"customers_id": customers_id, "name": "The great Plumbus"}

def create_customer(customer: Customer):
    pass