from typing import Optional

from schemas.job_application import ShowJobApplication

from  .users import ShowUser
from .base_class import BaseModel
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
    job_id:int
    status:str=''

#this will be used to validate data while creating a Job
class InterviewCreate(InterviewBase):
    pass
    
class ListInterview(InterviewBase):
    id:int




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
    application:ShowJobApplication=None
    applicant:ShowUser
    # class Config():  #to convert non dict obj to json
    #     orm_mode = True