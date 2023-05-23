from fastapi import Depends
from sqlalchemy.orm import Session
from db.models.jobs import JobApplication
from db.session import get_db

from schemas.jobs import JobCreate
from db.models.jobs import Job,Interview



def create_new_job(job: JobCreate,db: Session,owner_id:int):
    job_object = Job(**job.dict(),owner_id=owner_id)
    db.add(job_object)
    db.commit()
    db.refresh(job_object)
    return job_object


def retreive_job(id:int,db:Session):
    item = db.query(Job).filter(Job.id == id).first()
    return item

def list_jobs(db : Session):    #new
        
        jobs = db.query(Job).all()#.filter(Job.is_active == True)#.all()#.filter(Job.is_active == True)
  
        return jobs 
def filter_jobs(db:Session,ownerId:int):
    jobs=db.query(Job).filter(Job.owner_id==ownerId)
    return jobs

 

def update_job_by_id(id:int, job: JobCreate,db: Session,owner_id):
    existing_job = db.query(Job).filter(Job.id == id)
    if not existing_job.first():
        return 0
    job.__dict__.update(owner_id=owner_id)  #update dictionary with new key value of owner_id
    existing_job.update(job.__dict__)
    db.commit()
    return 1

def delete_job_by_id(id: int,db:Session,owner_id):
    existing_job = db.query(Job).filter(Job.id == id)
    if not existing_job.first():
        return 0
    existing_job.delete(synchronize_session=False)
    db.commit()
    return 1

def search_job(query: str, db: Session):
    jobs = db.query(Job).filter(Job.title.contains(query))
    return jobs


# def update_job_by_id(id:int, job: JobCreate,db: Session,owner_id):
#     existing_job = db.query(Job).filter(Job.id == id)
#     if not existing_job.first():
#         return 0
#     job.__dict__.update(owner_id=owner_id)  #update dictionary with new key value of owner_id
#     existing_job.update(job.__dict__)
#     db.commit()
#     return 1

def all_applications(db:Session):
    applications=db.query(JobApplication).filter(JobApplication.status=='') or []
 
    return applications

def all_interviews(db:Session):
    interviews=db.query(Interview).all() 
    return interviews

def add_application(db:Session,application:JobApplication,owner_id:int=None):
    print(application )
    create_application= JobApplication(**application.dict(),applicant_id=owner_id)
    db.add(create_application)
    db.commit()
    db.refresh(create_application)
    return create_application


def update_application_by_id(id:int,db:Session,application:JobApplication,owner_id:int=None):
    existing_application= db.query(JobApplication).filter(JobApplication.id == id)
    existing_application.update(application.__dict__)
    db.commit()
    db.refresh(existing_application)
    return existing_application

def add_interviews(interview:Interview,db:Session):
    
    interviews=Interview(**interview.dict())
    db.add(interviews)
    db.commit()
    db.refresh(interviews)
    return interviews
