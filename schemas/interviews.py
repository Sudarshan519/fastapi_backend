from typing import Optional
from pydantic import BaseModel
from datetime import date,datetime,time
    # id = Column(Integer,primary_key = True, index=True)
    # title = Column(String(50),nullable= False)
    # applicant_id= Column(Integer,ForeignKey("user.id",),default=1,nullable=False)
    # applicant= relationship("User",back_populates="interview")
    # date=Column(Date)
    # time=Column(Time)

#shared properties
class InterviewBase(BaseModel):
    title : Optional[str] = None 
    date:Optional[date]
    time:Optional[time]
    applicant_id:int

#this will be used to validate data while creating a Job
class InterviewCreate(InterviewBase):
 
    # id:int
    title:Optional[str]
    date:date
    time:time
    applicant_id:int
    job_id:int
    status:str




    # title : str
    # company : str 
    # location : str
    # description : str 
    
#this will be used to format the response to not to have id,owner_id etc
class ShowInterview(InterviewBase):
    id: int
    title : str 
    company: str 
    company_url : Optional[str]
    city : str 
    date_posted : date
    description : Optional[str]

    class Config():  #to convert non dict obj to json
        orm_mode = True