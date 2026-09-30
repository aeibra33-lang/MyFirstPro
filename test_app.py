# we will test out flask app functions here
from app import app
import pytest
#testing the flask endpoint ("/jobs/<int:id>") {the get_job_by_id() in flask}
def test_get_job_found():
    client=app.test_client()
    data={
        "company":"Amazon",
        "location":"USA",
        "role":"AI Engineer",
        "salary":600000,
        "status":"Accepted"
    }
    post_response=client.post("/jobs",json=data)
    jobId=post_response.json["ID"]    
    
    response=client.get(f'/jobs/{jobId}')
    assert response.status_code==200
    assert response.json["company"]=="Amazon"
    assert response.json["location"]=="USA"
    assert response.json["role"]=="AI Engineer"
    assert response.json["salary"]==600000
    assert response.json["status"]=="Accepted"
def test_get_job_not_found():
    client=app.test_client()

    response=client.get("/jobs/800")
    assert response.status_code==404
    assert response.json["error"]=="Job doesn't exist!"

# testing the post endpoint:

def test_post_job_ok():
    client=app.test_client()
    data={
            "company":"Amazon",
            "location":"USA",
            "role":"AI Engineer",
            "salary":600000,
            "status":"Accepted"
        }
    response=client.post("/jobs",json=data)
    assert response.status_code==201

def test_post_job_missing_fields():
    client=app.test_client()
    data={
        "company":"Amazon",
        "location":"USA",
        "role":"AI Engineer",
    }
    response=client.post("/jobs",json=data)
    assert response.status_code==400
    assert response.json["error"]=="Missing field/s"    
    
def test_post_not_integer_salary():
    client=app.test_client()
    data={
            "company":"Amazon",
            "location":"USA",
            "role":"AI Engineer",
            "salary":"Siuuu",
            "status":"Interview"
        }
    response=client.post("/jobs",json=data)

    assert response.status_code==400
    assert response.json["error"]=="Invalid salary!"    
def test_salary_negative():
    client=app.test_client()
    data={
             "company":"Amazon",
             "location":"USA",
             "role":"AI Engineer",
             "salary":-900,
             "status":"Interview"
         }  
    response=client.post("/jobs",json=data)
    assert response.status_code==400 
    assert response.json["error"]=="Invalid salary!" 
def test_all_fields_but_salary_empty():
    client=app.test_client()
    data={
                "company":" ",
                "location":" ",
                "role":" ",
                "salary":5,
                "status":" "
            }    
    response=client.post("/jobs",json=data)
    assert response.status_code==400
    assert response.json["error"]=="Invalid fields!"
def test_all_fields_but_salary_not_string():
    client=app.test_client()
    data={
                "company":34,
                "location":3,
                "role":33,
                "salary":5,
                "status":33
            }    
    response=client.post("/jobs",json=data)
    assert response.status_code==400
    assert response.json["error"]=="Invalid fields!"
def test_status_not_valid():
    client=app.test_client()
    data={
                "company":"OpenAI",
                "location":"USA",
                "role":"ML Engineer",
                "salary":300,
                "status":"Pussy"
            }    
    response=client.post("/jobs",json=data)
    assert response.status_code==400
    assert response.json["error"]=="Status must be (Interview- Accepted- Rejected- Offer)"
def test_empty_salary():
    client=app.test_client()
    data={
        "company":"OpenAI",
        "location":"USA",
        "role":"ML Engineer",
        "salary":" ",
        "status":"Pussy"
    }
    response=client.post("/jobs",json=data)
    assert response.json["error"]=="Invalid salary!"
    assert response.status_code==400 

#testing patch endpoint:
def test_invalid_status():
    client=app.test_client()
    data={
        "company":"OpenAI",
        "location":"USA",
        "role":"ML Engineer",
        "salary":12000,
        "status":"Interview"
        }
    newData={
        "company":"OpenAI",
        "location":"USA",
        "role":"ML Engineer",
        "salary":12000,
        "status":"Oklahoma"
        }
    post_response=client.post("/jobs", json=data)
    jobId=post_response.json["ID"]
    response=client.patch(f'/jobs/{jobId}',json=newData)
    assert response.status_code==400
    assert response.json["error"]=="Status must be (Interview- Accepted- Rejected- Offer)"
def test_id_doesnt_exist():
    client=app.test_client()
    data={
        "company":"OpenAI",
        "location":"USA",
        "role":"ML Engineer",
        "salary":400,
        "status":"Interview"
    }
    response=client.patch("/jobs/4000",json=data)
    assert response.status_code==404
    assert response.json["error"]=="ID doesn't exist"
def test_invalid_salary():
    client=app.test_client()    
    data={
            "company":"OpenAI",
            "location":"USA",
            "role":"ML Engineer",
            "salary":12000,
            "status":"Interview"
            }
    newData={
            "company":"OpenAI",
            "location":"USA",
            "role":"ML Engineer",
            "salary":"",
            "status":"Interview"
            }
    post_response=client.post("/jobs", json=data)
    jobId=post_response.json["ID"]
    response=client.patch(f'/jobs/{jobId}',json=newData)
    assert response.status_code==400
    assert response.json["error"]=="some field/s are not valid!"
def test_all_good():
    client=app.test_client()
    data={
                "company":"OpenAI",
                "location":"USA",
                "role":"ML Engineer",
                "salary":12000,
                "status":"Interview"
                }
    newData={
                "company":"OpenAI",
                "location":"USA",
                "role":"ML Engineer",
                "salary":1000000,
                "status":"Interview"
                }
    post_response=client.post("/jobs", json=data)
    jobId=post_response.json["ID"]
    response=client.patch(f'/jobs/{jobId}',json=newData)
    assert response.status_code==200


# testing the delete endpoint:
def test_deleted_succesfully():
    client=app.test_client()
    data={
        "company":"OpenAI",
        "location":"USA",
        "role":"ML Engineer",
        "salary":12000,
        "status":"Interview"
    }
    post_response=client.post("/jobs", json=data)
    jobId=post_response.json["ID"]
    response=client.delete(f'/jobs/{jobId}')
    assert response.status_code==200

def test_deleting_non_existing_job():
    client=app.test_client()
    response=client.delete(f'/jobs/1000')
    assert response.status_code==404
    assert response.json["error"]=="Job doesn't exist"    

#testing get all jobs:
def test_all_jobs_fetched():
    # client=app.test_client()
    # response=client.get("/jobs")
    # assert response.json==[]   
    # assert response.status_code==200 
    
    client = app.test_client()
    
    # Create 2 jobs
    job1_data = {
        "company":"OpenAI",
        "location":"USA",
        "role":"ML Engineer",
        "salary":12000,
        "status":"Interview"
         }
    job2_data = {
        "company":"Amazon",
        "location":"USA",
        "role":"ML Engineer",
        "salary":12000,
        "status":"Accepted"
        }

    
    response1 = client.post("/jobs", json=job1_data)
    response2 = client.post("/jobs", json=job2_data)
    
    # Get all jobs
    response = client.get("/jobs")
    
    # Assert
    assert response.status_code == 200

    
     
    

  



