# class JobApplication(Base):
#     id = Column(Integer,primary_key = True, index=True)
#     applicant_id= Column(Integer,ForeignKey("user.id",),default=1,nullable=False)
#     designation = Column(String(50),nullable= False)
#     address = Column(String(50),nullable= False)
#     city = Column(String(50),nullable= False)
#     email= Column(String(50),nullable= False)
#     phone = Column(String(50),nullable= False)
#     job_id=Column(Integer,ForeignKey("job.id"),default=1)


from typing import Optional
from pydantic import BaseModel
from datetime import date,datetime


#shared properties
class JobApplicationBase(BaseModel):
    email : Optional[str] = None
    phone : Optional[str] = None
    designation : Optional[str] = None
    city : Optional[str] = "Remote"
    address : Optional[str] = None
    date_posted : Optional[date] = datetime.now().date()
    job_id:int

#this will be used to validate data while creating a Job
class JobApplicationCreate(JobApplicationBase):
    email:str
    phone:str
    designation:str
    city:str
    address:str
    job_id:int

    # title : str
    # company : str 
    # location : str
    # description : str 
    
#this will be used to format the response to not to have id,owner_id etc
class ShowJobApplication(JobApplicationBase):
    id: int
    title : str 
    company: str 
    company_url : Optional[str]
    city : str 
    date_posted : date
    description : Optional[str]

    class Config():  #to convert non dict obj to json
        orm_mode = True