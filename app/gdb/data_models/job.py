#!/usr/bin/env python3
"""Job Sheet Data Management."""
import time, uuid

faked_data = [{'4b886871-b3c5-4003-b8b2-528a76490c68': {'job_id': '4b886871-b3c5-4003-b8b2-528a76490c68', 'status': 'O', 'client_id': 'Spanarchian', 'houseNumber': '1', 'location': 'DT1 1SS', 'service_req': [1], 'created_ts': 1626729546.245023, 'created': 'Mon Jul 19 22:19:06 2021', 'required_date': '', 'time': '', 'budget': '15.00'}}]
        


def create_job(jobRequest):
    now = time.time()
    id = str(uuid.uuid4())
    print(f" ID = {id}")
    job = {}
    job["job_id"] = id
    job["status"]= 'O'
    job["client_id"]= jobRequest["client_id"]
    job["houseNumber"]= jobRequest["houseNumber"]
    job["location"]= jobRequest["location"]
    job["service_req"]= jobRequest["service_req"]
    job["created_ts"]= now
    job["created"]= time.ctime(now)
    job["required_date"]= jobRequest["required_date"]
    job["time"]= jobRequest["time"] 
    job["budget"] = jobRequest["budget"]
    
    faked_data.append({id: job})
    return faked_data

# create_job(external_data)


def retrive_job(ref=0):
    print("Triggered retrive_job")
    reqst = faked_data
    for clnt in reqst:
        print(f"clnt = {clnt[ref]}")
        if clnt[ref] != {}:
            return clnt[ref]
        else:
            return f"{ref} was notfound"
            
