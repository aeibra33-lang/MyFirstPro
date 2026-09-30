function delete_all(){
    if(confirm("Are you sure you want to delete everything?? data can't be restored anymore!!!")){
        fetch("/jobs",{method:"DELETE"})
        .then(function(response){
            load_jobs(current_search, current_status)
        })

    }
}
    
        function create_job_api(jobData){
            return fetch("/jobs",{method:"POST",body:JSON.stringify(jobData),headers:{"Content-Type":"application/json"}})
            .then(function(response){
                if(!response.ok){
                return response.json()
                    .then(function(data){
                        throw new Error(`Error: ${data["error"]}`)
                    })
                }
                return response.json()
            })
        }
        function update_job_api(id,jobData){
            return fetch(`/jobs/${id}`,{method:"PATCH", body:JSON.stringify(jobData), headers:{"Content-Type":"application/json"}})
                .then(function(response){
                    if(!response.ok){
                        return response.json().then(function(data){
                            throw new Error(`Error: ${data["error"]}`)
                        })
                    }
                    return response.json()
                })
        }         
        let search_field=document.querySelector("#search-field")
        let search_button=document.querySelector("#search-btn")
        let clear_search_button=document.querySelector("#clear-search-btn")
        let status_filter=document.querySelector("#status-filter")
        let error_display=document.querySelector("#error-message")
        let container=document.querySelector("#jobs-container")
        let button=document.querySelector("#submit-btn")
        let form=document.querySelector("#job-form")
        let cancel_button=document.querySelector("#cancel-btn")
        let editting_id=null
        let current_search=null
        let current_status=null
        function load_jobs(current_search=null, current_status=null){
            error_display.textContent=""
            container.innerHTML="Loading jobs..."
            let url
            if (current_search===null && current_status===null){
                url="/jobs"
            }
            else if(current_status===null){
                url=`/jobs?search=${current_search}`
            }
            else if(current_search===null){
                url=`/jobs?status=${current_status}`
            }
            else{
                url=`/jobs?search=${current_search}&status=${current_status}`
            }
            fetch(url)
            .then(function(response) {
                if(!response.ok){
                    return response.json()
                    .then(function(data){
                        throw new Error(`Error: ${data["error"]}`)
                    })
                }
                return response.json()
            })    
            .then(function(data){
                container.innerHTML=""
                if(data.length === 0){
                    if(current_search===null && current_status===null){
                        container.textContent="No Jobs yet!"
                        return
                    }
                    else{
                        container.textContent="No matching results!"
                        return
                    }
                }
                for(let job of data){
                   let jobDiv=document.createElement("div")
                   let id_p=document.createElement("p")
                   let company_p=document.createElement("p")
                   let role_p=document.createElement("p")
                   let status_p=document.createElement("p")
                   let location_p=document.createElement("p")
                   let salary_p=document.createElement("p")
                   let delete_b=document.createElement("button")
                   let edit_b=document.createElement("button")
                   id_p.textContent=`ID: ${job["id"]}`
                   company_p.textContent=`Compnay: ${job["company"]}`
                   role_p.textContent=`Role: ${job["role"]}`
                   status_p.textContent=`Status: ${job["status"]}`
                   location_p.textContent=`location: ${job["location"]}`
                   salary_p.textContent=`Salary: ${job["salary"]}`
                    delete_b.textContent="DELETE"
                    delete_b.onclick=function(){delete_job(job["id"])}
                    edit_b.textContent="EDIT"
                    edit_b.onclick= function(){edit_job(job["id"])}
                    delete_b.className="delete-btn"
                    edit_b.className="edit-btn"
                    jobDiv.className="job-container"
                    jobDiv.appendChild(id_p)
                    jobDiv.appendChild(company_p)
                    jobDiv.appendChild(role_p)
                    jobDiv.appendChild(status_p)
                    jobDiv.appendChild(location_p)
                    jobDiv.appendChild(salary_p)
                    jobDiv.appendChild(delete_b)
                    jobDiv.appendChild(edit_b)
                    container.appendChild(jobDiv)
                }     
            })
            .catch(function(error){
                container.innerHTML=""
                error_display.textContent=error.message
            })
        }
        load_jobs(current_search, current_status)    
        function delete_job(id){
            if(confirm("Are you sure?!")){
                fetch(`/jobs/${id}`,{method:"DELETE"})
                .then(function(response){
                    if(!response.ok){
                        return response.json().then(function(data){
                            throw new  Error(`Error: ${data["error"]}`)
                        })
                    }
                    load_jobs(current_search, current_status)
                })
                .catch(function(error){
                    error_display.textContent=error.message
                })
            }
        }    
        function edit_job(id){
            fetch(`/jobs/${id}`)
            .then(function(response){
                if(!response.ok){
                    return response.json()
                    .then(function(data){
                        throw new Error(`Error: ${data["error"]}`)
                    })
                }
                editting_id=id
                cancel_button.hidden=false
                button.textContent="UPDATE"
                return response.json()
            })
            .then(function(data){
                let company_field=document.querySelector("#company")
                let role_field=document.querySelector("#role")
                let location_field=document.querySelector("#location")
                let status_field=document.querySelector("#status")
                let salary_field=document.querySelector("#salary")
                company_field.value=data["company"]
                role_field.value=data["role"]
                location_field.value=data["location"]
                status_field.value=data["status"]
                salary_field.value=data["salary"]
            })
            .catch(function(error){
                error_display.textContent=error.message
            })
        }            
            form.addEventListener("submit", function(event){
                event.preventDefault()
                let company=document.querySelector("#company").value
                let location=document.querySelector("#location").value
                let role=document.querySelector("#role").value
                let salary=document.querySelector("#salary").value
                let status=document.querySelector("#status").value
                let jobData={
                    "company":company,
                    "location":location,
                    "role":role,
                    "salary":salary,
                    "status":status,
                }
                let fields=["company", "location", "role", "salary", "status"]
                for(let field of fields){
                    if(jobData[field]===""){
                        error_display.textContent=`${field} can't be empty!`
                        return
                    }
                    }
                    if(Number.isNaN(Number(jobData["salary"]))){
                        error_display.textContent="Salary must be a number"
                        return 
                    }
                    if(Number.isInteger(Number(jobData["salary"]))===false){
                        error_display.textContent="Salary must be a whole number"
                        return
                    }
                    button.disabled=true        
                    jobData["salary"]=Number(jobData["salary"])
                    error_display.textContent=""
                    if(editting_id===null){
                        create_job_api(jobData)
                        .then(function(data){
                            form.reset()
                            load_jobs(current_search, current_status)
                            button.disabled=false
                        })
                        .catch(function(error){
                            button.disabled=false
                            error_display.textContent=error.message
                        })
                    }
                    else{
                        update_job_api(editting_id,jobData)
                        .then(function(data){
                             form.reset()
                             load_jobs(current_search, current_status)
                             button.disabled=false
                             cancel_button.hidden=true
                             button.textContent="ADD"
                             editting_id=null
                        })
                        .catch(function(error){
                         error_display.textContent=error.message
                         button.disabled=false
                        })
                    }
                })  
            cancel_button.addEventListener("click", function(){
                cancel_button.hidden=true
                form.reset()
                editting_id=null
                button.textContent="ADD"
                error_display.textContent=""
            })
            search_button.addEventListener("click", function(){
                if(search_field.value!=""){
                    current_search=search_field.value
                    clear_search_button.hidden=false
                    load_jobs(current_search, current_status)
                }
                else{
                    clear_search_button.hidden=true
                    error_display.textContent="Search field can't be empty"
                }
            })
            clear_search_button.addEventListener("click", function(){
                current_search=null
                clear_search_button.hidden=true
                load_jobs(current_search, current_status)
                search_field.value=""
            })
            status_filter.addEventListener("change",function(){
                current_status=status_filter.value
                if(current_status===""){
                    current_status=null
                    load_jobs(current_search, current_status)
                }
                else{
                    load_jobs(current_search, current_status)
                }
            })
                   
                   
                    
                    

