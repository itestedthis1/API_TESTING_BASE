import time, uuid, logging
from json import dumps, loads
from typing import List, Optional
from pydantic import BaseModel
from app.gdb.helper.graph import get_gdb
gdbservice = get_gdb('prod')

class Customer(BaseModel):
    id: str
    status : bool
    title : str
    CompanyReg : int
    RegisteredAddress : str
    password : str
    signup_ts: float
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




def register_customer(appliction):
    '''Create customer profile with metadata'''
    now = time.time()
    id = str(uuid.uuid4())
    print(f" ID = {id}")
    customer = {}
    customer["id"] = id
    customer["active"]= True
    customer["assigned"]= False
    customer["CompanyReg"]= appliction["CompanyReg"]
    customer["RegisteredAddress"]= appliction["RegisteredAddress"]
    customer["password"]= appliction["password"]
    customer["signup_ts"]= now
    customer["joined"]= time.ctime(now)
    customer["AreasCovered"]=appliction["AreasCovered"]
    customer["WorkingDays"]=appliction["WorkingDays"]
    customer["services"]=appliction["services"]
    resp = process_registration(customer)
    if resp != 'error':
        update_database(customer)
        return {"status": 200, "msg":f"profile created for {customer['id']}" }
    else:
        print(f"application failed - {resp}")
        return {"status": 500, "error":f"ERROR: application failed - {resp}"}
                
    
    
def process_registration(application: Customer):
    '''Ensure that the application is unique - based on email & address'''
    if application["id"] == "":
        logging.error(f"ID error in {application}")
        return 'error'
    else:
        return application


def update_database(customer_profile: Customer):
    '''Update Database: with processed and verified customer profile.'''
    print(f"Start registration for register_customer : {customer_profile}")
    query = """
    WITH $json as data
    UNWIND data as q
    MERGE (customer :CUSTOMER {id:q.id}) ON CREATE
    SET customer.title = q.title, customer.status = q.status, customer.CompanyReg = q.CompanyReg, 
    customer.RegisteredAddress = q.RegisteredAddress,  customer.password = q.password, 
    customer.signup_ts = q.signup_ts, customer.joined = q.joined,
    customer.AreasCovered = q.AreasCovered,
    customer.WorkingDays = q.WorkingDays,
    customer.services = q.services 
    """

    print(f"Start graph execution for customer {customer_profile}")
    print(f"Graph execution with query: {query}")
    gdbservice.run(query,json=customer_profile)
    print(f"Complete graph execution for customer {customer_profile}")
    return {"success":"customer created successfully", "query":query}

def get_all_customers():
    print("Start retrieval of ALL CUSTOMERS:")
    query = """
    match (customer:CUSTOMER) return customer as clt
    """
    resp = dumps(gdbservice.run(query).data())
    print(f"resp {resp}")
    result = loads(resp)
    print(f"result {result}")
    data = result[0]['clt']
    print(f"data {data}")
    print(f"result of graph execution for job {result}")
    return {"profile":data, "query":query}


def get_customer_profile(customer_id):
    # print(f"Start retrieval of customer: {customer_id}")
    query = """
    match (customer :CUSTOMER) where customer.id = $customer_id return customer as clt
    """
    # print(f"Start graph execution for retrieving customer {customer_id}")
    # print(f"Graph execution with query: {query}")
    resp = dumps(gdbservice.run(query, customer_id=customer_id).data())
    print(f"resp {resp}")
    result = loads(resp)
    print(f"result {result}")
    data = result[0]['clt']
    print(f"data {data}")
    print(f"Complete graph execution for customer {customer_id}")
    print(f"result of graph execution for customer {result}")
    return {"profile":data, "query":query}



if __name__ == '__main__':
    pass