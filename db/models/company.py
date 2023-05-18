from sqlalchemy import Column,Integer, String,Boolean, ForeignKey
from sqlalchemy.orm import relationship

from db.base_class import Base


class Company(Base):
    id = Column(Integer,primary_key=True,index=True)
    email = Column(String(60),nullable=False,unique=True,index=True)
    is_active = Column(Boolean(),default=True)  
    owner_id =  Column(Integer,ForeignKey("user.id",),default=1)
    owner = relationship("User",back_populates="company_owner")