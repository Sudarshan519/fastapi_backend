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
    
    # company = relationship("Company",back_populates="company_owner")  

# class Employee(User):
#     # company
#     # user id
#     pass

# class JobSeeker(User):
#     pass

# class Owner(User):
#     pass

