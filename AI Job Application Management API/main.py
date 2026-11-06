from fastapi import FastAPI,HTTPException,Path
from pydantic import BaseModel,Field,EmailStr
from typing import Annotated,Literal

app=FastAPI(
    title="AI job Application API",
    description="Manage candidate job applications"
)

class JobApplication(BaseModel):
    candidate_name:Annotated[str,Field(min_length=3,max_length=50)]

    email:Annotated[EmailStr,Field(min_length=5)]

    """we stored the skill in the list"""
    skills:Annotated[list[str],Field(min_length=0,max_length=40)]

    experience:Annotated[int,Field(ge=0,le=40)]

    job_role:Literal[
        "Python Developer",
        "AI Engineer",
        "Data Scientist",
        "ML Engineer"
        ]  
    """less than equal to(<=)"""
    expected_salary:Annotated[int,Field(gt=0,le=50000000)]

    status:Literal[
        "Applied",
        "shortlisted",
        "Rejected"
    ]="Applied"




class Job(BaseModel):

    job_title: Annotated[str, Field(min_length=3, max_length=50)]

    company_name: Annotated[str, Field(min_length=3, max_length=50)]

    job_role: Literal[
        "Python Developer",
        "AI Engineer",
        "Data Scientist",
        "ML Engineer"
    ]

    location: Annotated[str, Field(min_length=2)]

    salary: Annotated[int, Field(gt=0, le=50000000)]

    openings: Annotated[int, Field(ge=1, le=1000)]

    job_type: Literal[
        "Full-time",
        "Part-time",
        "Internship"
    ]

# Temporary database
applications = {
    1: {
        "candidate_name": "Pratik Shelke",
        "email": "pratik@gmail.com",
        "skills": ["Python", "FastAPI", "Machine Learning"],
        "experience": 1,
        "job_role": "AI Engineer",
        "expected_salary": 600000,
        "status": "Applied"
    }
}

jobs = {
    101: {
        "job_title": "Python Developer",
        "company_name": "Infosys",
        "job_role": "Python Developer",
        "location": "Pune",
        "salary": 600000,
        "openings": 5,
        "job_type": "Full-time"
    }
}

"""GET-welcome"""
@app.get("/")
def home():
    return{"message":"Welcome to AI Job Application API"}

"""show data"""
@app.get("/applications")
def get_applications():
    return applications

"""get application id"""
@app.get("/applications/{application_id}")
def get_application(
    application_id: Annotated[int, Path(gt=0)]
):
    data = applications

    if application_id not in data:
        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )

    return data[application_id]

"""POST-Apply for job"""
@app.post("/applications")
def apply_job(application:JobApplication):
    application_id=max(applications.keys(),default=0)+1
    applications[application_id]=application.model_dump()
    return{
        "message":"job application submmit successfully",
        "application_id":application_id,
        "application":applications[application_id]
    }


"""get job opening"""
@app.get("/jobs")
def get_jobs():
    return jobs

"""access the job informartion"""
@app.get("/jobs/{job_id}")
def get_job(job_id:Annotated[int,Path(gt=0)]):
    data=jobs
    if job_id not in data:
        raise HTTPException(status_code=404,detail="job not found")
    return data[job_id]


"""candidate post api"""
@app.post("/jobs")
def apply_job(job:Job):
    job_id=max(jobs.keys(),default=100)+1
    jobs[job_id]=job.model_dump()
    return{
        "message":"Job created successfully",
        "job_id":job_id,
        "job_details":jobs[job_id]
    }




    
