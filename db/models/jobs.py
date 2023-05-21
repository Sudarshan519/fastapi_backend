from sqlalchemy import Column, Integer, String, Boolean,Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from db.base_class import Base
from schemas.jobs import JobCreate

class Job(Base):
    id = Column(Integer,primary_key = True, index=True)
    title = Column(String(256),nullable= False)
    company = Column(String(256),nullable=False)
    company_url = Column(String(256))
    location = Column(String(256),nullable = False)
    description = Column(String(256),nullable=False)
    date_posted = Column(Date)
    is_active = Column(Boolean(),default=True)
    owner_id =  Column(Integer,ForeignKey("user.id",),default=1)
    seats=Column(Integer,default=3)
    salary=Column(String(128),default="")
    owner = relationship("User",back_populates="jobs")
    # applications=relationship('JobApplication',back_populates='jobs')

class JobApplication(Base):
    id = Column(Integer,primary_key = True, index=True)
    applicant_id= Column(Integer,ForeignKey("user.id",),default=1,nullable=False)
    designation = Column(String(50),nullable= False)
    address = Column(String(50),nullable= False)
    city = Column(String(50),nullable= False)
    email= Column(String(50),nullable= False)
    phone = Column(String(50),nullable= False)
    job_id=Column(Integer,ForeignKey("job.id"),default=1)
#     # job=relationship("Job",back_populates="applications")
    # applicant=relationship("User",back_populates="jobs")
#     status=Column(String(50),default="")

class Interview(Base):
    id = Column(Integer,primary_key = True, index=True)
    title = Column(String(50),nullable= False)
    date=Column(Date)

# class Education(Base):
#     id = Column(Integer,primary_key = True, index=True)
#     title = Column(String(50),nullable= False)
#     desc = Column(String(256),nullable= False)
#     start_date=Column(Date)
#     end_date=Column(Date)
#     user_id= Column(Integer,ForeignKey("user.id",),default=1)
#     user=relationship("User",back_populates="education")

# class Achievements(Base):
#     id = Column(Integer,primary_key = True, index=True)
#     title = Column(String(50),nullable= False)
#     desc = Column(String(256),nullable= False)

# class Skills(Base):
#     id = Column(Integer,primary_key = True, index=True)
#     title = Column(String(50),nullable= False)
#     desc = Column(String(256),nullable= False)