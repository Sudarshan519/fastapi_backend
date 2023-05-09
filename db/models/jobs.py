from sqlalchemy import Column, Integer, String, Boolean,Date, ForeignKey
from sqlalchemy.orm import relationship

from db.base_class import Base


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


def update_job_by_id(id:int, job: JobCreate,db: Session,owner_id):
    existing_job = db.query(Job).filter(Job.id == id)
    if not existing_job.first():
        return 0
    job.__dict__.update(owner_id=owner_id)  #update dictionary with new key value of owner_id
    existing_job.update(job.__dict__)
    db.commit()
    return 1