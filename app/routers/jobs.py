"""Job Route."""

from fastapi import APIRouter, Depends, HTTPException
from typing import List
from pydantic import BaseModel

from ..dependencies import get_token_header

class Job(BaseModel):
    id : str
    active : bool
    assigned : bool
    client_id: str
    servicesReq: List[ int ] = []
    date_required: str
    time_required: str
    assignedTo: str
    assignedOn: str
    worksheet: str
    class Config:
        '''Docstring here.'''
        schema_extra = {
            "example": {
                "id": "7f644301-e3f1-4752-90d5-99fbfad95uh8",
                "active" : True,
                "assigned" : False,
                "client_id" : 'client_guid',
                "date_required" : "01/01/22",
                "time_required" : "13:45",
                "assigned_to" : "",
                "assigned_on" : "",
                "worksheet" : "",
                }
        }


router = APIRouter(
    prefix="/jobs",
    tags=["jobs"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

def find_job(ref):
    if ref not in fake_job_db:
        raise HTTPException(status_code=404, detail="Customers not found")
    return {"result": fake_job_db[ref]}


fake_job_db = {"7f644301-e3f1-4752-90d5-99fbfad95uh8": {
                "id": "7f644301-e3f1-4752-90d5-99fbfad95uh8",
                "active" : True,
                "assigned" : False,
                "client_id" : 'client_guid',
                "date_required" : "01/01/22",
                "time_required" : "13:45",
                "assigned_to" : "",
                "assigned_on" : "",
                "worksheet" : "",
                },
               "7f644301-e3f1-4752-90d5-99fbfad99xx9":{
                "id": "7f644301-e3f1-4752-90d5-99fbfad99xx9",
                "active" : True,
                "assigned" : True,
                "client_id" : 'client_guid',
                "date_required" : "01/01/22",
                "time_required" : "13:45",
                "assigned_to" : "customer_guid",
                "assigned_on" : "10/10/21",
                "worksheet" : "7f644301-e3f1-4752-90d5-99fbabc12xx3",
               }}

@router.get("/")
async def get_jobs():
    return fake_job_db


@router.get("/register/")
async def rregister_jobs(job: Job):
    return {"job_ref": job.id, "assigned_to": job.assigned_to}


@router.get("/jobs/{jobs_id}")
async def read_jobs(jobs_id: str):
    return {"jobs_id": jobs_id}


