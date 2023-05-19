# from sqlalchemy import Column, ForeignKey, Integer
# from backend.db.base_class import Base
# from sqlalchemy.orm import relationship

# class JobSeeker(Base):
#     user_id=Column(Integer,ForeignKey("user.id",),default=1)    
#     user = relationship("User",back_populates="job_seeker")