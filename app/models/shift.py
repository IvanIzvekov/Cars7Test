from sqlalchemy import Column, Integer, TIMESTAMP, ForeignKey
from app.models.base import Base

class Shift(Base):
    __tablename__ = "shifts"

    id = Column(Integer, primary_key=True)
    start_time = Column(TIMESTAMP, nullable=False)
    end_time = Column(TIMESTAMP)
    operator_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
