"""Work Route."""

from fastapi import APIRouter, Depends, HTTPException
from typing import List
from pydantic import BaseModel

from ..dependencies import get_token_header


class Work(BaseModel):
    id : str
    active : bool
    assigned : bool
    client_id: str
    servicesReq: List[ int ] = []
    date_required: str
    time_required: str
    customer_id: str
    assignedTo: str
    assignedOn: str
    jobsheet: str
    class Config:
        '''Docstring here.'''
        schema_extra = {
            "example": {
                "id": "7f644301-e3f1-4752-90d5-99fbfad95uh8",
                "active" : True,
                "assigned" : True,
                "client_id" : 'client_guid',
                "date_required" : "01/01/22",
                "time_required" : "13:45",
                "customer_id": "7f644301-e3f1-4752-90d5-99fbfad95ty9",
                "assigned_to" : "Spick N Span",
                "assigned_on" : "12/12/21",
                "jobsheet" : "7f966301-e3f1-4752-90d5-99fbfji56ji9",
                }
        }



router = APIRouter(
    prefix="/works",
    tags=["works"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

fake_works_db = {"plumbus": {"name": "Plumbus"}, "gun": {"name": "Portal Gun"}}


@router.get("/")
async def read_works():
    return fake_works_db


@router.get("/{works_id}")
async def read_item(works_id: str):
    if works_id not in fake_works_db:
        raise HTTPException(status_code=404, detail="works Item not found")
    return {"name": fake_works_db[works_id]["name"], "works_id": works_id}


@router.put(
    "/{works_id}",
    responses={403: {"description": "Operation forbidden"}},
)
async def update_item(works_id: str):
    if works_id != "plumbus":
        raise HTTPException(
            status_code=403, detail="You can only update the item: plumbus"
        )
    return {"works_id": works_id, "name": "The great Plumbus"}