import time, uuid, logging
import datetime
from json import dumps, loads
from typing import List, Optional
from pydantic import BaseModel
from app.gdb.helper.graph import get_gdb

gdbservice = get_gdb('prod')

class Job(BaseModel):
    id: str
    active : bool
    assigned: bool
    requestedBy: str #jobID
    requestedFor: str #date required to be done 
    requiredService: int
    requested_ts: float
    assignedWorkSheet: str #id of the worksheet for the job to be done
    class Config:
        '''Docstring here.'''
        schema_extra = {
            "example": {
                "id": "9g644301-e3f1-4752-90d5-99fbfad99xy4",
                "active" : True,
                "assigned" : False,
                "requestedBy" : 'Any Clean',
                "requestedFor" : "23/08/2021",
                "requiredService" : 3,
                "signup_ts": None,
                "assignedWorkSheet": ""
            }}




def register_job(appliction):
    '''Create job profile with metadata'''
    now = time.time()
    id = str(uuid.uuid4())
    print(f" ID = {id}")
    job = {}
    job["id"] = id
    job["active"]= True
    job["assigned"]= False
    job["requestedBy"]= appliction["requestedBy"]
    job["requestedFor"]= appliction["requestedFor"]
    # job["requestedWeekday"]= datetime.datetime(2021,8,3).weekday()
    job["requiredService"]= appliction["requiredService"]
    job["requested_ts"]= now
    job["requested"]= time.ctime(now)
    job['assignedWorkSheet']= ""
    resp = process_registration(job)
    if resp != 'error':
        update_database(job)
        return {"status": 200, "msg":f"profile created for {job['id']}" }
    else:
        print(f"application failed - {resp}")
        return {"status": 500, "error":f"ERROR: application failed - {resp}"}
                
    
    
def process_registration(application: Job):
    '''Ensure that the application is unique - based on email & address'''
    if application["id"] == "":
        logging.error(f"ID error in {application}")
        return 'error'
    else:
        return application


def update_database(job_profile: Job):
    '''Update Database: with processed and verified job profile.'''
    print(f"Start registration for register_job : {job_profile}")
    query = """
    WITH $json as data
    UNWIND data as q
    Match (client :CLIENT) where client.id = q.requestedBy
    MERGE (job :JOB {id:q.id}) ON CREATE
    SET job.active = q.active, job.assigned = q.assigned, job.requestedBy = q.requestedBy, 
    job.requestedFor = q.requestedFor,  job.requiredService = q.requiredService, 
    job.requested_ts = q.requested_ts, job.requested = q.requested,
    job.assignedWorkSheet = q.assignedWorkSheet
    CREATE (job)-[r :REQUESTEDBY {requested:q.requested}]->(client)
    """

    print(f"Start graph execution for job {job_profile}")
    print(f"Graph execution with query: {query}")
    gdbservice.run(query,json=job_profile)
    print(f"Complete graph execution for job {job_profile}")
    return {"success":"job created successfully", "query":query}


def get_job_profile(job_id):
    # print(f"Start retrieval of job: {job_id}")
    query = """
    match (job :JOB) where job.id = $job_id return job as clt
    """
    # print(f"Start graph execution for retrieving job {job_id}")
    # print(f"Graph execution with query: {query}")
    resp = dumps(gdbservice.run(query, job_id=job_id).data())
    print(f"resp {resp}")
    result = loads(resp)
    print(f"result {result}")
    data = result[0]['clt']
    print(f"data {data}")
    # print(f"Complete graph execution for job {job_id}")
    # print(f"result of graph execution for job {result}")
    return {"profile":data, "query":query}


if __name__ == '__main__':
    pass
