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
    owner = relationship("User",back_populates="jobs")


