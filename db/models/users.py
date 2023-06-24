from enum import Enum
from sqlalchemy import Column,Integer, String,Boolean, ForeignKey
from sqlalchemy.orm import relationship

from db.base_class import Base

class UserType(str, Enum):
    jobseeker='jobseeker'
    employee='employee'
    employer='employer'

class User(Base):
    id = Column(Integer,primary_key=True,index=True)
    username = Column(String(60),unique=True,nullable=False)
    email = Column(String(60),nullable=False,unique=True,index=True)
    hashed_password = Column(String(256),nullable=False)
    is_job_seeker=Column(Boolean(),default=False)
    is_employee=Column(Boolean(),default=False)
    is_employer=Column(Boolean(),default=False)
    is_active = Column(Boolean(),default=True)
    is_superuser = Column(Boolean(),default=False)
    jobs = relationship("Job",back_populates="owner")
    # facebook_id=Column(String(256),nullable=True)
    # google_id=Column(String(256),nullable=True)
    # phone=Column(String(128),nullable=False)
    jobapplication=relationship("JobApplication",back_populates="applicant")
    interview=relationship("Interview",back_populates="applicant")
    # company = relationship("Company",back_populates="company_owner")  

class Profile(Base):
    id = Column(Integer,primary_key=True,index=True)
    firstname=Column(String(128),nullable=False)
    middlename=Column(String(128),nullable=False)
    lastname=Column(String(128),nullable=False)
    profile_pic=Column(String(256),nullable=False)



# class Employee(User):
#     # company
#     # user id
#     pass

# class JobSeeker(User):
#     pass

# class Owner(User):
#     pass

