from flask import Flask, jsonify, request, render_template
from database import add_job, initialise,  update_job, delete_job, view_jobs, get_job_by_id, get_job_by_status, get_job_by_status_and_keyword, search, delete_all
import sqlite3
app=Flask(__name__)
initialise()
#LOAD WEB PAGE
@app.route("/")
def load_page():
    page=render_template("index.html")
    return page
#CHECK IF THE  JOBS WE GOT ARE VALID:
def check_if_jobs_valid(theJobs):
    if theJobs is None:
        return jsonify({
            "error":"Database error"
        }), 500
    else:
        theJobs=[dict(job) for job in theJobs]
        return jsonify(theJobs), 200  
# GET ALL JOBS
@app.route("/jobs", methods=["GET"])
def get_jobs():
    keyword=request.args.get("search")
    status_keyword=request.args.get("status")
    # if we didn't send any params then we just get all the jobs
    if keyword==None and status_keyword==None:
        jobs=view_jobs()
        result=check_if_jobs_valid(jobs)
        return result
    #then we check the search keyword so we can send the matching resutls:
    elif keyword!=None and status_keyword==None:
        jobs=search(keyword)
        result=check_if_jobs_valid(jobs)
        return result
    #here we check only if the status param is valid
    elif status_keyword!=None and keyword==None:
        jobs=get_job_by_status(status_keyword)
        result=check_if_jobs_valid(jobs)
        return result
    else:
        jobs=get_job_by_status_and_keyword(keyword, status_keyword)
        return check_if_jobs_valid(jobs)
    
  
# GET ONE JOB WITH A SPECIFIC ID
@app.route("/jobs/<int:job_id>", methods=["GET"])
def get_job(job_id):
    try:
        job=get_job_by_id(job_id)
        if job is None:
            return jsonify({
                "error":"Job doesn't exist!"
            }),404
        job=dict(job)
        return jsonify(job)
    except sqlite3.Error:
        return jsonify({
            "error":"Database error"
        }), 500
    
    
#CREATE JOB
@app.route("/jobs", methods=["POST"])
def create_job():
    data=request.get_json(silent=True)
    if data is None:
        return jsonify({
            "error":"Invalid json"
        }), 400
    missing_fields=["company","location","role","salary","status" ]
    for field in missing_fields :
        if field not in data:
            return jsonify({
                "error":"Missing field/s"
            }),400
    if  not isinstance(data["salary"],int) or  data["salary"]<0:
        return jsonify({
            "error":"Invalid salary!"
        }), 400
    
    text_missing_fields=["company","location","role","status"]
    for field in text_missing_fields:
        if not isinstance(data[field],str) or not data[field].strip():
            return jsonify({
                "error":"Invalid fields!"
            }), 400  
    if field=="status":
        if data["status"] not in["Interview","Accepted","Rejected","Offer"]:
            return  jsonify({
                "error":"Status must be (Interview- Accepted- Rejected- Offer)"
            }), 400       
    company=data["company"]
    location=data["location"]
    role=data["role"]
    salary=data["salary"]
    status=data["status"]
    job_id=add_job(company, location, role, salary, status)
    return jsonify({
        "ID":job_id,
        "company":company,
        "location":location,
        "role":role,
        "salary":salary,
        "status":status,
    }), 201

# MODIFY JOB
@app.route("/jobs/<int:job_id>", methods=["PATCH"])
def update_job_route(job_id):
    field_map = {
    "company": 1,
    "role": 2,
    "status": 3,
    "location": 4,
    "salary": 5
}
    data=request.get_json(silent=True)
    if data is None:
        return jsonify({
            "error":"Invalid json!!"
        }), 400
    is_found=False
    updated_fields={}
    valid_fields=[]
    for field in data:
        if field in field_map:
            is_found=True
            if field=="salary":
                if isinstance(data[field], int) and data[field]>=0 :
                    valid_fields.append("salary")
                    updated_fields["salary"]=data[field]
            elif field =="company":
                if isinstance(data[field], str) and data[field].strip():
                    updated_fields["company"]=data[field]
                    valid_fields.append("company")
            elif field =="role":
                if isinstance(data[field], str) and data[field].strip():
                    updated_fields["role"]=data[field]
                    valid_fields.append("role")    
            elif field =="location":
                if isinstance(data[field], str) and data[field].strip():
                    updated_fields["location"]=data[field]
                    valid_fields.append("location")
            elif field =="status":
                if isinstance(data[field], str) and data[field].strip():
                    updated_fields["status"]=data[field]
                    valid_fields.append("status")
    if "status" in data:
            if data["status"] not in["Interview","Accepted","Rejected","Offer"]:
                return  jsonify({
                    "error":"Status must be (Interview- Accepted- Rejected- Offer)"
                }), 400                
    if is_found==True: 
        for field in data:
            if field in valid_fields:
                affected_rows=update_job(job_id, field_map.get(field), data[field])
                if not affected_rows:
                    return jsonify({
                    "error":"ID doesn't exist"
                    }), 404
            else:
                return jsonify({
                    "error":"some field/s are not valid!"
                }), 400
        return jsonify({
            "ID":job_id,
            "updated":updated_fields
        }), 200    
    else:
        return jsonify({
            "error":"invalid field!!!!"
        }), 400    
                    
# DELETE JOB            
@app.route("/jobs/<int:job_id>", methods=["DELETE"])
def delete_job_route(job_id):
    rows_affected=delete_job(job_id)
    if rows_affected:
        return jsonify({
            "id":job_id
        }),200
    else:
        return jsonify({
            "error":"Job doesn't exist"
        }), 404

@app.route("/jobs",methods=["DELETE"])
def delete_everything():
  result=delete_all()
  return jsonify(result)  
