from sqlalchemy import Column, Integer, String, Numeric
from app.models.base import Base

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True)
    last_name = Column(String(50), nullable=False)
    first_name = Column(String(50), nullable=False)
    second_name = Column(String(50))
    position = Column(String(30), nullable=False)
    status = Column(String(20), nullable=False)
    salary = Column(Numeric, nullable=False)
