from app.gdb.services import job
import pytest

test_application = {
    "requestedBy": "478ea65d-afc4-434f-800a-bb50cecb90eb",  # clientID
    "requestedFor": '25/09/2021',  # Date required to be done
    "requiredService": 3
}

test_profile = {
    'id': "ae94ee37-b21e-407c-a4b7-81973e0b75c3",
    'active': True,
    'assigned': False,
    'requestedBy': "478ea65d-afc4-434f-800a-bb50cecb90eb",  # clientID
    'requestedFor': '25/09/2021',  # Date required to be done
    'requiredService': 3,
    'requested_ts': 1627571049.827422,
    'assignedWorkSheet': ""
}

test_job_id = "5cfb4380-80c3-4b95-93b3-4d8abed114c6"

test_job_profile = {
        'requestedFor': '25/09/2021',
        'requestedBy': '478ea65d-afc4-434f-800a-bb50cecb90eb',
        'requested': 'Thu Sep 23 12:01:02 2021',
        'assignedWorkSheet': '',
        'active': True,
        'requiredService': 3,
        'assigned': False,
        'requested_ts': 1632394862.3132648,
        'id': '5cfb4380-80c3-4b95-93b3-4d8abed114c6'}


def test_register_job():
    '''Test that the metadata is added to the application'''
    actual = job.register_job(test_application)
    print(f"Actual resp = {actual}")
    assert actual['status'] == 200, "Status-Code not as expected"
    assert actual["msg"].startswith("profile created for"),\
        "Name not as expected"


def test_process_registration_valid():
    '''Test that the registration is unique.'''
    actual = job.process_registration(test_profile)
    print(f"Actual resp  =  {actual}")
    assert actual['id'] != "", "No ID ref generated"
    assert actual["requestedBy"] == "478ea65d-afc4-434f-800a-bb50cecb90eb",\
        "Name not as expected"


def test_process_registration_invalid():
    '''Test when the registration id is missing.'''
    expected = 'error'
    test_profile["id"] = ""
    actual = job.process_registration(test_profile)
    print(f"Actual resp  =  {actual}")
    assert actual == expected, f"Expected Error got {actual}"


@pytest.mark.skip("TODO - Database updates")
def test_update_database():
    '''Verify the cypher query is created and executed.'''
    expected_success = 'job created successfully'
    expected_query = """
    WITH $json as data
    UNWIND data as q
    Match (client :CLIENT) where client.id = q.requestedBy
    MERGE (job :JOB {id:q.id}) ON CREATE
    SET job.active = q.active,
    job.assigned = q.assigned,
    job.requestedBy = q.requestedBy,
    job.requestedFor = q.requestedFor,
    job.requiredService = q.requiredService,
    job.requested_ts = q.requested_ts,
    job.requested = q.requested,
    job.assignedWorkSheet = q.assignedWorkSheet
    CREATE (job)-[r :REQUESTEDBY {requested:q.requested}]->(client)
    """
    actual = job.update_database(test_profile)
    print(f"Actual resp  =  {actual}")
    assert actual['success'] == expected_success,\
        f"Expected Error got {actual['success']}"
    assert actual['query'] == expected_query,\
        f"Expected Error got {actual['query']}"


def test_get_job_profile():
    '''Verify you can collect job profile from job id.'''
    expected_profile = test_job_profile
    actual = job.get_job_profile(test_job_id)
    print(f"Actual resp  =  {actual['profile']}")
    # assert actual['success'] == expected_success,\
    # f"Expected Error got {actual['success']}"
    assert actual['profile'] == expected_profile,\
        f"Expected Error got {actual['profile']}"
