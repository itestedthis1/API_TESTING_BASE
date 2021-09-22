
# # Get active jobs not yet assigned
# matchingQuery = """
#     match (j :JOB) where j.assigned==false AND j.active==true
#     with j
#     match (c :CUSTOMER) where j.serviceRquired in c.services AND j.loc in c.AreasCovered
#     merge (j)-[o :OFFERED {dateOffered: '01/01/21'}]->(c)

# """






# def complete_exchange(customer_id, job_id):
#     pass    
    
# def process_exchange():
#     pass


# def update_database():
#     pass


# def update_work():
#     pass


